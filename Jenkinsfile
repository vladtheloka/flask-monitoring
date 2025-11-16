pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'flask-monitoring:latest'
        DOCKER_NETWORK = 'devops-net'
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        PYTHONPATH = "/app"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                    export DOCKER_BUILDKIT=1
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Code Quality: Black + Flake8') {
            steps {
                sh '''
                    docker run --rm \
                    --network $DOCKER_NETWORK \
                    -v "$PWD":/app \
                    -w /app \
                    -e PYTHONPATH=/app \
                      $DOCKER_IMAGE \
                    bash -c "flake8 app && black app"
                '''
            }
        }

        /*stage('Run Tests + Coverage') {
            steps {
                sh '''
                    docker run --rm \
                        --network $DOCKER_NETWORK \
                        -v "$PWD":/app \
                        -w /app \
                        -e PYTHONPATH=/app \
                        $DOCKER_IMAGE \
                        python3 -m pytest \
                            --disable-warnings --maxfail=1 \
                            --cov=app --cov-report=xml:coverage.xml \
                            app/tests
                '''
            }
        }*/

        /*stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                                -Dsonar.sources=app \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.host.url=$SONAR_HOST_URL
                        '''
                        }
                }
            }
        }*/

        /*stage('Quality Gate') {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }*/
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
