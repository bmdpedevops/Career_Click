pipeline {
    agent any
    environment {
        GIT_CREDENTIALS = credentials('github-credentials') // GitHub credentials
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:bmdpedevops/Career_Click.git',
                    credentialsId: 'github-ssh-key'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    sh 'python3 -m venv venv'
                    sh 'source venv/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'source venv/bin/activate && pytest'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t fastapi-app .'
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
                    sh 'docker tag fastapi-app amukthamalyadagaje/fastapi-app:latest'
                    sh 'docker push amukthamalyadagaje/fastapi-app:latest'
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@ec2-54-208-197-251.compute-1.amazonaws.com "
                    docker pull amukthamalyadagaje/fastapi-app:latest &&
                    docker run -d -p 80:80 amukthamalyadagaje/fastapi-app:latest"
                    """
                }
            }
        }

        stage('Clean Up') {
            steps {
                cleanWs()
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}