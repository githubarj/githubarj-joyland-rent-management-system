pipeline {
    agent any

    environment {
        // Dynamically passed secrets from Jenkins credentials
        DJANGO_SECRET_KEY = credentials('DJANGO_SECRET_KEY')
        DB_NAME          = credentials('DB_NAME')
        DB_USER          = credentials('DB_USER')
        DB_PASSWORD      = credentials('DB_PASSWORD')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Prepare .env') {
            steps {
                script {
                    sh '''
                    cat > backend/.env <<EOF
                    DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
                    DB_NAME=$DB_NAME
                    DB_USER=$DB_USER
                    DB_PASSWORD=$DB_PASSWORD
                    DB_HOST=db
                    DB_PORT=5432
                    REDIS_URL=redis://redis:6379/0
                    EOF
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose -f docker-compose.yml build backend frontend'
            }
        }

        stage('Run Tests') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        script {
                            sh 'docker-compose run --rm backend python manage.py test'
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        script {
                            sh 'docker-compose run --rm frontend npm test -- --watchAll=false'
                        }
                    }
                }
            }
        }

        stage('Deploy Docker Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                echo "Checking backend health..."
                curl -f http://localhost:8000/ || exit 1
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
        success {
            echo "Build, test, and deploy succeeded!"
        }
        failure {
            echo "Something went wrong. Check the logs above."
        }
    }
}
