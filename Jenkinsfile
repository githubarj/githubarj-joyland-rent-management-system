
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

    // ── Triggers ──────────────────────────────────

    triggers {
        // Listen for GitHub webhook
        githubPush()
        // Also check GitHub every 5 minutes as backup
        pollSCM('H/5 * * * *')
    }

    // ── Options ───────────────────────────────────
    options {

        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Fail if pipeline takes longer than 30 mins
        timeout(time: 30, unit: 'MINUTES')
        // Don't run same branch concurrently
        disableConcurrentBuilds()
        // Add timestamps to console output
        timestamps()
    }

    // ── Stages ────────────────────────────────────
    stages {

        //  Checkout

        stage('Checkout') {
            steps {
                // Clean workspace before checkout
                cleanWs()

                checkout scm

                // Print what commit we're building
                sh 'git log --oneline -5'
            }
        }


        //  Run Tests in Parallel

        stage('Test') {
            when {
                anyOf {
                    branch 'development'
                    branch 'main'
                    expression { env.BRANCH_NAME.startsWith('release/') }
                    expression { env.CHANGE_ID }
                }
            }
            // Run backend and frontend tests at same time
            parallel {

                // ── Backend Tests ──────────────
                stage('Backend Tests') {
                    steps {
                        script {

                            docker.image('python:3.11-slim').inside(

                                '--network ci-network'
                            ) {
                                dir('backend') {
                                    sh '''
                                        pip install --upgrade pip -q
                                        pip install -r requirements/dev.txt -q

                                        # Formatting check
                                        black --check --diff .

                                        # Import order check
                                        isort --check-only --diff .

                                        # Linting
                                        flake8 .

                                        # Security scan
                                        bandit -r apps/ -c pyproject.toml

                                        # Tests with coverage
                                        pytest \
                                          --cov=. \
                                          --cov-report=xml:coverage.xml \
                                          --cov-report=html:htmlcov \
                                          --cov-report=term-missing \
                                          --cov-fail-under=80 \
                                          -v
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

                            // Archive test results
                            junit(
                                testResults: 'backend/test-results/*.xml',
                                allowEmptyResults: true
                            )
                        }
                    }
                }

                // ── Frontend Tests ─────────────
                stage('Frontend Tests') {
                    steps {
                        script {
                            docker.image("node:${NODE_VERSION}-alpine").inside {
                                dir('frontend') {
                                    sh '''
                                        npm ci --silent

                                        # Formatting check
                                        npx prettier --check src/

                                        # Linting
                                        npm run lint

                                        # Tests with coverage
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

                // ── Security Scan ──────────────
                stage('Security Scan') {
                    steps {
                        script {
                            // Run Trivy security scanner
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

        // Build Docker Images
        // Only runs if ALL tests passed
        // Only on main branch

        stage('Build Images') {
            // Only build on main branch pushes
            when {
                anyOf {
                   branch 'main'
                    branch 'development'
                }
            }

            steps {
                script {
                    // Login to GitHub Container Registry
                    sh "echo ${GHCR_TOKEN} | docker login ghcr.io -u ${GITHUB_ACTOR} --password-stdin"

                    // Build and tag with git commit SHA
                    def gitSha = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()

                    // Build backend
                    sh """
                        docker build \
                          -f docker/backend/Dockerfile \
                          --target production \
                          -t ${REGISTRY}/${IMAGE_NAME}/backend:${gitSha} \
                          -t ${REGISTRY}/${IMAGE_NAME}/backend:latest \
                          ./backend
                    """

                    // Build frontend
                    sh """
                        docker build \
                          -f docker/frontend/Dockerfile \
                          --target production \
                          --build-arg REACT_APP_API_URL=https://yourapp.com \
                          -t ${REGISTRY}/${IMAGE_NAME}/frontend:${gitSha} \
                          -t ${REGISTRY}/${IMAGE_NAME}/frontend:latest \
                          ./frontend
                    """

                    // Push both images
                    sh """
                        docker push ${REGISTRY}/${IMAGE_NAME}/backend:${gitSha}
                        docker push ${REGISTRY}/${IMAGE_NAME}/backend:latest
                        docker push ${REGISTRY}/${IMAGE_NAME}/frontend:${gitSha}
                        docker push ${REGISTRY}/${IMAGE_NAME}/frontend:latest
                    """
                }
            }
        }


        //  Deploy
        // Only after successful build
        // Only on main branch

        stage('Deploy') {
            when {
                branch 'main'
            }

            steps {
                script {
                    // Since Jenkins runs ON the server
                    // we deploy directly - no SSH needed
                    sh """
                        cd ${APP_DIR}

                        # Pull latest images
                        docker compose -f docker-compose.prod.yml pull

                        # Start new containers
                        docker compose -f docker-compose.prod.yml up -d \
                          --remove-orphans \
                          --no-build

                        # Run database migrations
                        docker compose -f docker-compose.prod.yml exec -T \
                          backend python manage.py migrate

                        # Collect static files
                        docker compose -f docker-compose.prod.yml exec -T \
                          backend python manage.py collectstatic --noinput

                        # Clean up old images
                        docker image prune -f
                    """
                }
            }
        }

        // Health Check

        stage('Health Check') {
            when {
                branch 'main'
            }

            steps {
                script {
                    // Wait for app to start
                    sleep(20)

                    // Retry health check 5 times
                    retry(5) {
                        sh '''
                            response=$(curl -s -o /dev/null -w "%{http_code}" \
                              http://localhost/api/health/)

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

    // ── Post Actions ──────────────────────────────

   // slacksend maybe
}
