pipeline {
    agent any

    environment {
        PYTHON_VERSION  = '3.11'
        NODE_VERSION    = '18'
        APP_DIR         = '/opt/app'
        REGISTRY        = 'ghcr.io'
        IMAGE_NAME      = 'githubarj/githubarj-joyland-rent-management-system'

        DJANGO_SECRET_KEY = credentials('django-secret-key')
        DB_NAME           = credentials('db-name')
        DB_USER           = credentials('db-user')
        DB_PASSWORD       = credentials('db-password')
        GHCR_TOKEN        = credentials('ghcr-token')
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                sh 'git log --oneline -5'
            }
        }

        stage('Test') {
            // Run on main, development, release/*, or PRs
            when {
                anyOf {
                    branch 'main'
                    branch 'development'
                    expression { env.BRANCH_NAME.startsWith('release/') }
                    changeRequest()
                }
            }
            parallel {

                stage('Backend Tests') {
                    steps {
                        script {
                            docker.image('python:3.11-slim').inside('--network ci-network') {
                                dir('backend') {
                                    sh '''
                                        pip install --upgrade pip -q
                                        pip install -r requirements/dev.txt -q
                                        black --check --diff .
                                        isort --check-only --diff .
                                        flake8 .
                                        bandit -r apps/ -c pyproject.toml
                                        pytest --cov=. --cov-report=xml:coverage.xml --cov-report=html:htmlcov --cov-report=term-missing --cov-fail-under=80 -v
                                    '''
                                }
                            }
                        }
                    }
                    post {
                        always {
                            publishHTML(target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'backend/htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'Backend Coverage Report'
                            ])
                            junit(testResults: 'backend/test-results/*.xml', allowEmptyResults: true)
                        }
                    }
                }

                stage('Frontend Tests') {
                    steps {
                        script {
                            docker.image("node:${NODE_VERSION}-alpine").inside {
                                dir('frontend') {
                                    sh '''
                                        npm ci --silent
                                        npx prettier --check src/
                                        npm run lint
                                        CI=true npm run test:coverage
                                    '''
                                }
                            }
                        }
                    }
                    post {
                        always {
                            publishHTML(target: [
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'frontend/coverage/lcov-report',
                                reportFiles: 'index.html',
                                reportName: 'Frontend Coverage Report'
                            ])
                        }
                    }
                }

                stage('Security Scan') {
                    steps {
                        script {
                            sh '''
                                docker run --rm \
                                  -v /var/run/docker.sock:/var/run/docker.sock \
                                  -v $(pwd):/project \
                                  aquasec/trivy:latest fs \
                                  --severity CRITICAL,HIGH \
                                  --exit-code 1 \
                                  /project
                            '''
                        }
                    }
                }
            }
        }

        stage('Build Images') {
            // Run on main, development, release/*, or PRs
            when {
                anyOf {
                    branch 'main'
                    branch 'development'
                    expression { env.BRANCH_NAME.startsWith('release/') }
                    changeRequest()
                }
            }
            steps {
                script {
                    def gitSha = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    sh "echo ${GHCR_TOKEN} | docker login ghcr.io -u ${GITHUB_ACTOR} --password-stdin"

                    // Build backend
                    sh """
                        docker build -f docker/backend/Dockerfile --target production \
                          -t ${REGISTRY}/${IMAGE_NAME}/backend:${gitSha} \
                          -t ${REGISTRY}/${IMAGE_NAME}/backend:latest ./backend
                    """

                    // Build frontend
                    sh """
                        docker build -f docker/frontend/Dockerfile --target production \
                          --build-arg REACT_APP_API_URL=https://yourapp.com \
                          -t ${REGISTRY}/${IMAGE_NAME}/frontend:${gitSha} \
                          -t ${REGISTRY}/${IMAGE_NAME}/frontend:latest ./frontend
                    """
                }
            }
        }

        stage('Deploy') {
            // Only deploy on main branch
            when {
                branch 'main'
            }
            steps {
                script {
                    sh """
                        cd ${APP_DIR}
                        docker compose -f docker-compose.prod.yml pull
                        docker compose -f docker-compose.prod.yml up -d --remove-orphans --no-build
                        docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate
                        docker compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput
                        docker image prune -f
                    """
                }
            }
        }

        stage('Health Check') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sleep(20)
                    retry(5) {
                        sh '''
                            response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/health/)
                            if [ "$response" != "200" ]; then
                                echo "Health check failed: $response"
                                sleep 10
                                exit 1
                            fi
                            echo "Health check passed!"
                        '''
                    }
                }
            }
        }
    }
}
