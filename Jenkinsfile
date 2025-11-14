pipeline {
    agent any

    environment {
        PROJECT_NAME = 'flask-monitoring'
        DOCKER_IMAGE = 'flask-monitoring:latest'
        DOCKER_NETWORK = 'devops-net'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        SONAR_HOST_URL = 'http://sonarqube:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t $DOCKER_IMAGE ."
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running pytest with coverage...'
                sh '''
                docker run --rm -v "$PWD":/app -w /app $DOCKER_IMAGE \
                  python3 -m pip install --no-cache-dir -r requirements.txt
                docker run --rm -v "$PWD":/app -w /app $DOCKER_IMAGE \
                  python3 -m pytest --cov=app --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_AUTH_TOKEN')]) {
                        withSonarQubeEnv('sonarqube') {
                            sh '''
                            docker run --rm \
                              --network $DOCKER_NETWORK \
                              -e SONAR_HOST_URL=$SONAR_HOST_URL \
                              -e SONAR_TOKEN=$SONAR_AUTH_TOKEN \
                              -v $PWD:/usr/src \
                              sonarsource/sonar-scanner-cli:latest \
                              -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                              -Dsonar.sources=. \
                              -Dsonar.python.coverage.reportPaths=coverage.xml \
                              -Dsonar.sourceEncoding=UTF-8
                            '''
                        }
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            echo "\033[1;31m❌ Quality Gate failed: ${qg.status}\033[0m"
                            error "Pipeline aborted due to Quality Gate"
                        } else {
                            echo "\033[1;32m✅ Quality Gate passed\033[0m"
                        }
                    }
                }
            }
        }

        /*stage('Push Docker Image (Optional)') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    docker login -u $DOCKER_USER -p $DOCKER_PASS
                    docker tag $DOCKER_IMAGE $DOCKER_USER/$DOCKER_IMAGE
                    docker push $DOCKER_USER/$DOCKER_IMAGE
                    '''
                }
            }
        }*/
    }

    post {
        success {
            echo 'Pipeline succeeded ✅'
        }
        failure {
            echo 'Pipeline failed ❌'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
