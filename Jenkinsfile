pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-monitoring:latest'
        DOCKER_NETWORK = 'devops-net'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        PATH = "/opt/sonar-scanner/bin:${PATH}"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running pytest with coverage...'
                sh '''
                docker run --rm --network $DOCKER_NETWORK $DOCKER_IMAGE \
                    python3 -m pytest --cov=app --cov-report=xml /app/tests
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=flask-monitoring \
                            -Dsonar.sources=app
                        """
                    }
                }
                }
            }
        

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
