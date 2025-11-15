pipeline {
    agent any

    environment {
        DOCKER_IMAGE     = 'flask-monitoring:latest'
        DOCKER_NETWORK   = 'devops-net'
        SONAR_PROJECT_KEY = 'flask-monitoring'
        SONAR_HOST_URL   = 'http://sonarqube:9000'
        PATH = "/opt/sonar-scanner/bin:${PATH}"
    }

    stages {

        stage('Build Image') {
            steps {
                echo "Building Docker image with BuildKit..."
                sh '''
                    export DOCKER_BUILDKIT=1
                    docker build \
                        --cache-from=type=local,src=/root/.cache/pip \
                        --cache-to=type=local,dest=/root/.cache/pip \
                        -t $DOCKER_IMAGE .
                '''
            }
        }

        stage('Lint & Format') {
            steps {
                echo "Running flake8 and black check..."
                sh '''
                    docker run --rm \
                        -v "$PWD":/app \
                        -w /app \
                        $DOCKER_IMAGE \
                        bash -c "
                            flake8 app && \
                            black --check app
                        "
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running pytest with coverage..."
                sh '''
                    docker run --rm \
                        --network $DOCKER_NETWORK \
                        -v "$PWD":/app \
                        -v pytest-cache:/app/.pytest_cache \
                        -w /app \
                        -e PYTHONPATH=/app \
                        $DOCKER_IMAGE \
                        python3 -m pytest \
                            --disable-warnings \
                            --maxfail=1 \
                            --cov=app \
                            --cov-report=xml:coverage.xml \
                            app/tests
                '''
            }
        }

        stage("SonarQube Analysis") {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'

                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                                -Dsonar.sources=app \
                                -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed."
        }
    }
}
