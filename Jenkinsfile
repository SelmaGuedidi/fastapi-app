@Library('my-shared-library') _
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
                    buildDockerImage(DOCKER_IMAGE)
                }
            }
        }

        stage('Tag and Push Docker Image') {
            steps {
                container('shell') {
                    pushDockerImage(DOCKER_IMAGE, DOCKERHUB_REPO)
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                container('shell') {
                    deployToKubernetes('k8s/deployment.yaml', 'k8s/service.yaml')
                }
            }
        }
    }
}
