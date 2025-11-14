pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-monitoring:latest'
        DOCKER_NETWORK = 'devops-net'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'flask-monitoring'
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
                script {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_AUTH_TOKEN')]) {
                        echo 'Running SonarQube scan...'
                        sh '''
                        docker run --rm --network $DOCKER_NETWORK \
                          -e SONAR_HOST_URL=$SONAR_HOST_URL \
                          -e SONAR_TOKEN=$SONAR_AUTH_TOKEN \
                          -v "$PWD":/usr/src \
                          sonarsource/sonar-scanner-cli:latest \
                          -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                          -Dsonar.sources=/usr/src/app \
                          -Dsonar.language=py \
                          -Dsonar.sourceEncoding=UTF-8
                        '''
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
