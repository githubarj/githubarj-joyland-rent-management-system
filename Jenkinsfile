pipeline {
    agent any

    environment {
        APP_NAME = "joyland"
        SERVER_IP = "178.104.38.211"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        // ─── PR BUILD & TEST (no deploy) ──────────────────
        stage('PR - Build & Test') {
            when {
                changeRequest()
            }
            stages {

                stage('Inject PR Env') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                rm -f backend/.env.dev
                                cp $ENV_FILE backend/.env.dev
                                chmod 600 backend/.env.dev
                            '''
                        }
                    }
                }

                stage('Build PR Images') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml build \
                                    --build-arg REACT_APP_API_URL=http://${SERVER_IP}:8000 \
                                    --build-arg REACT_APP_ENV=development
                            '''
                        }
                    }
                }

                stage('Run Tests') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml run --rm backend \
                                    python manage.py test --noinput
                            '''
                        }
                    }
                }
            }
        }


        // ─── DEVELOPMENT DEPLOYMENT ────────────────────────
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
                                rm -f backend/.env.dev
                                cp $ENV_FILE backend/.env.dev
                                chmod 600 backend/.env.dev
                            '''
                        }
                    }
                }

                stage('Build Dev Images') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml build \
                                    --build-arg REACT_APP_API_URL=http://${SERVER_IP}:8000 \
                                    --build-arg REACT_APP_ENV=development
                            '''
                        }
                    }
                }

                stage('Deploy Dev') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml down --remove-orphans
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml up -d
                            '''
                        }
                    }
                }

                stage('Run Migrations - Dev') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-dev', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.dev.yml exec -T backend \
                                    python manage.py migrate --noinput
                            '''
                        }
                    }
                }
            }
        }

        // ─── PRODUCTION DEPLOYMENT ─────────────────────────
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
                                rm -f backend/.env.prod
                                cp $ENV_FILE backend/.env.prod
                                chmod 600 backend/.env.prod
                            '''
                        }
                    }
                }

                stage('Build Production Images') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-prod', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.prod.yml build \
                                    --build-arg REACT_APP_API_URL=http://${SERVER_IP}:9090 \
                                    --build-arg REACT_APP_ENV=production
                            '''
                        }
                    }
                }

                stage('Deploy Production') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-prod', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.prod.yml down --remove-orphans
                                docker compose --env-file $ENV_FILE -f docker-compose.prod.yml up -d
                            '''
                        }
                    }
                }

                stage('Run Migrations - Production') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-prod', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.prod.yml exec -T backend \
                                    python manage.py migrate --noinput
                            '''
                        }
                    }
                }

                stage('Collect Static Files') {
                    steps {
                        withCredentials([
                            file(credentialsId: 'joyland-env-prod', variable: 'ENV_FILE')
                        ]) {
                            sh '''
                                docker compose --env-file $ENV_FILE -f docker-compose.prod.yml exec -T backend \
                                    python manage.py collectstatic --noinput
                            '''
                        }
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
