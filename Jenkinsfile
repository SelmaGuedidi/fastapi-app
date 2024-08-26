properties([
    pipelineTriggers([
        githubPush()
    ])
])

pipeline {
    agent {
        kubernetes {
            cloud "minikube"
            label "shell"
            defaultContainer "shell"
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: shell
    image: docker:24.0.1
    command:
    - cat
    tty: true
  - name: dind
    image: docker:24.0.1-dind
    securityContext:
      privileged: true
  volumes:
  - name: docker-graph-storage
    emptyDir: {}
  """
        }
    }
    environment {
       
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials') // Docker Hub credentials in Jenkins
        DOCKER_IMAGE = "fastapi-app:latest"
        DOCKERHUB_REPO = "selmaguedidi/fastapi-app"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                container('shell') {
                    script {
                        sh 'docker info'
                        sh '''
                        docker build -t $DOCKER_IMAGE .
                        '''
                    }
                }
            }
        }

        stage('Tag and Push Docker Image') {
            steps {
                container('shell') {
                    script {
                        sh '''
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker tag $DOCKER_IMAGE $DOCKERHUB_REPO:latest
                        docker push $DOCKERHUB_REPO:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                container('shell') {
                    sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                container('shell') {
                    sh '''
                    kubectl rollout status deployment/fastapi-app-deployment
                    kubectl get pods
                    '''
                }
            }
        }
    }
}
