pipeline {
    agent any

    environment {
        PYTHON_VERSION  = '3.11'
        NODE_VERSION    = '18'
        APP_DIR         = "${WORKSPACE}" // Jenkins workspace
        REGISTRY        = 'ghcr.io'
        IMAGE_NAME      = 'githubarj/githubarj-joyland-rent-management-system'
        GITHUB_ACTOR = 'githubarj'

        // Jenkins credentials IDs
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

        stage('Prepare .env') {
            steps {
                withCredentials([
                    string(credentialsId: 'django-secret-key', variable:        'DJANGO_SECRET_KEY'),
                    string(credentialsId: 'db-name', variable: 'DB_NAME'),
                    string(credentialsId: 'db-user', variable: 'DB_USER'),
                    string(credentialsId: 'db-password', variable: 'DB_PASSWORD')
                ]) {
                    sh script: '''
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



        stage('Build & Deploy Docker') {
            when {
                anyOf {
                    branch 'main'
                    branch 'development'
                    changeRequest()
                }
            }
            steps {
                script {
                    // Login to GitHub Container Registry
                    sh "echo ${GHCR_TOKEN} | docker login ghcr.io -u ${GITHUB_ACTOR} --password-stdin"

                    // Build and deploy Docker Compose stack
                    sh """
                    docker compose -f docker-compose.yml down --remove-orphans
                    docker compose -f docker-compose.yml build
                    docker compose -f docker-compose.yml up -d
                    """
                }
            }
        }

        stage('Health Check') {
            when { branch 'main' }
            steps {
                script {
                    sleep(20)
                    retry(5) {
                        sh '''
                        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health/)
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

    post {
        always {
                cleanWs()
        }
    }
}
