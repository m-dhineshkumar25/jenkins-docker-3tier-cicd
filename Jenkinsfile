pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "cloudops-backend"
        FRONTEND_IMAGE = "cloudops-frontend"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Test") {
            steps {
                sh '''
                    docker compose config
                '''
            }
        }

        stage("Build Docker Images") {
            steps {
                sh '''
                    cp .env.example .env

                    docker build \
                        -t ${BACKEND_IMAGE}:${BUILD_NUMBER} \
                        ./backend

                    docker build \
                        -t ${FRONTEND_IMAGE}:${BUILD_NUMBER} \
                        ./frontend
                '''
            }
        }

        stage("Trivy Security Scan") {
            steps {
                sh '''
                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        ${BACKEND_IMAGE}:${BUILD_NUMBER}

                    trivy image \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        ${FRONTEND_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }

        stage("Deploy") {
            steps {
                sh '''
                    cp .env.example .env

                    docker compose down --remove-orphans || true

                    docker compose up -d --build

                    docker compose ps
                '''
            }
        }

        stage("Health Check") {
            steps {
                sh '''
                    sleep 10

                    curl -f http://localhost/api/health

                    curl -f http://localhost/api/projects

                    docker compose ps
                '''
            }
        }

        stage("Cleanup") {
            steps {
                sh '''
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            echo "CI/CD pipeline completed successfully."
        }

        failure {
            echo "CI/CD pipeline failed."
        }

        always {
            echo "Pipeline execution completed."
        }
    }
}
