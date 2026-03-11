pipeline {
    agent any

    environment {
        APP_NAME = "joyland"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ─── PR BUILD CHECK ────────────────────────────────
        // Runs on PRs targeting main, development, release/*
        // Builds and deploys to staging so reviewer can test
        stage('PR - Build & Deploy to Staging') {
            when {
                allOf {
                    changeRequest()
                    expression {
                        env.CHANGE_TARGET ==~ /release\/sprint-.*/
                    }
                }
            }
            stages {

                stage('Inject Staging Env') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-staging', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                ls -la
                                ls -la backend/ || echo "backend folder does not exist"
                                whoami
                                mkdir -p backend
                                cp $ENV_FILE backend/.env.staging
                                chmod 600 backend/.env.staging
                            '''
                        }
                    }
                }

                stage('Build Staging Images') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml build \
                                --build-arg REACT_APP_API_URL=http://${SERVER_IP}:9000 \
                                --build-arg REACT_APP_ENV=staging
                        '''
                    }
                }

                stage('Deploy to Staging') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml down --remove-orphans
                            docker compose -f docker-compose.staging.yml up -d
                        '''
                    }
                }

                stage('Run Migrations - Staging') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml exec -T backend \
                                python manage.py migrate --noinput
                        '''
                    }
                }

                stage('Tests') {
                    steps {
                        echo 'Tests will go here'
                        // sh 'docker compose -f docker-compose.staging.yml exec -T backend python manage.py test'
                        // sh 'docker compose -f docker-compose.staging.yml exec -T frontend yarn test'
                    }
                }
            }
        }

        // ─── DEVELOPMENT DEPLOYMENT ────────────────────────
        // Runs on every push to development branch
        stage('Deploy to Dev') {
            when {
                branch 'development'
                not { changeRequest() }
            }
            stages {

                stage('Inject Dev Env') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                mkdir -p backend
                                cp $ENV_FILE backend/.env.dev
                                chmod 600 backend/.env.dev
                            '''
                        }
                    }
                }

                stage('Build Dev Images') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.dev.yml build \
                                --build-arg REACT_APP_API_URL=http://${SERVER_IP}:8000 \
                                --build-arg REACT_APP_ENV=development
                        '''
                    }
                }

                stage('Deploy Dev') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.dev.yml down --remove-orphans
                            docker compose -f docker-compose.dev.yml up -d
                        '''
                    }
                }

                stage('Run Migrations - Dev') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.dev.yml exec -T backend \
                                python manage.py migrate --noinput
                        '''
                    }
                }
            }
        }

        // ─── RELEASE/STAGING DEPLOYMENT ────────────────────
        // Runs on every merge/push to release/sprint-* branches
        stage('Deploy to Staging on Release Merge') {
            when {
                allOf {
                    branch pattern: 'release/sprint-.*', comparator: 'REGEXP'
                    not { changeRequest() }
                }
            }
            stages {

                stage('Inject Staging Env') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-staging', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                mkdir -p backend
                                cp $ENV_FILE backend/.env.staging
                                chmod 600 backend/.env.staging
                            '''
                        }
                    }
                }

                stage('Build Staging Images') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml build \
                                --build-arg REACT_APP_API_URL=http://${SERVER_IP}:9000 \
                                --build-arg REACT_APP_ENV=staging
                        '''
                    }
                }

                stage('Deploy Staging') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml down --remove-orphans
                            docker compose -f docker-compose.staging.yml up -d
                        '''
                    }
                }

                stage('Run Migrations - Staging') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.staging.yml exec -T backend \
                                python manage.py migrate --noinput
                        '''
                    }
                }
            }
        }

        // ─── PRODUCTION DEPLOYMENT ─────────────────────────
        // Runs on every push/merge to main
        stage('Deploy to Production') {
            when {
                branch 'main'
                not { changeRequest() }
            }
            stages {

                stage('Inject Production Env') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-prod', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                mkdir -p backend
                                cp $ENV_FILE backend/.env.prod
                                chmod 600 backend/.env.prod
                            '''
                        }
                    }
                }

                stage('Build Production Images') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.prod.yml build \
                                --build-arg REACT_APP_API_URL=http://${SERVER_IP}:9090 \
                                --build-arg REACT_APP_ENV=production
                        '''
                    }
                }

                stage('Deploy Production') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.prod.yml down --remove-orphans
                            docker compose -f docker-compose.prod.yml up -d
                        '''
                    }
                }

                stage('Run Migrations - Production') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.prod.yml exec -T backend \
                                python manage.py migrate --noinput
                        '''
                    }
                }

                stage('Collect Static Files') {
                    steps {
                        sh '''
                            docker compose -f docker-compose.prod.yml exec -T backend \
                                python manage.py collectstatic --noinput
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded on branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipeline failed on branch: ${env.BRANCH_NAME}"
        }
        cleanup {
            sh 'docker image prune -f'
        }
    }
}
