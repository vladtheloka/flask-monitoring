#!/usr/bin/groovy

pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_PROJECT_KEY = 'restmon-sonar-project'
        IMAGE_NAME = 'restmon'
        TAG = 'latest'
        CONTAINER = 'restmon_sigterm_test'
    }

    stages {
        stage('Build Docker image') {
            steps {
                sh """
                     export DOCKER_BUILDKIT=1
                     docker build -t ${IMAGE_NAME}:${TAG} .
                """
            }
        }

        stage('Lint (inside Docker)') {
            steps {
                sh("docker run --rm ${IMAGE_NAME}:${TAG} bash -c ' black . && flake8 . --ignore=E501'")
            }
        }

        stage('Run Unit Tests') {
            steps {
                script  {
                    /* groovylint-disable-next-line NestedBlockDepth */
                    docker.image("${IMAGE_NAME}:${TAG}").withRun('-u root') {   c ->
                        sh "docker exec ${c.id} python3 -m pytest -v \
                            --cov=restmon \
                            --cov-config=.coveragerc \
                            --cov-report=xml:/app/coverage.xml \
                            tests"
                        sh "docker cp ${c.id}:/app/coverage.xml coverage.xml"
                        echo '=== Coverage files ==='
                        sh 'ls -lah coverage.xml'
                    }
                }
            }
        }

        stage('Integration Tests') {
            steps {
                sh './run_int_test.sh'
            }
        }

        stage('SIGTERM lifecycle') {
            steps {
                sh """
                docker run --rm -d \
                -p 5000:5000 \
                --name ${CONTAINER} \
                ${IMAGE_NAME}:${TAG}
                """
                sh './wait_for_container.sh http://localhost:5000/health/ready 40'

                sh 'python3 -m pytest -c /dev/null -v tests_integration/test_sigterm.py'

                sh "docker stop '${CONTAINER}' || True"
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                        sh """
                            ${tool('SonarScanner')}/bin/sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                -Dsonar.sources=restmon \
                                -Dsonasr.tests=tests \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.sourceEncoding=UTF-8 \
                                -Dsonar.python.version=3.12 \
                                -Dsonar.tests=tests \
                                -Dsonar.scanner.skipJreProvisioning=true \
                                -Dsonar.scanner.caches.directory=.sonar/cache
                        """
                }
            }
        }

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
            cleanWs() // Clean workspace after build
        }
    }
}
