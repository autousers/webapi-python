pipeline {
    agent none
    stages {
      stage('PullCode') {
        agent {
          node {
            label 'covanly-linux'
          }
        }
        steps {
          echo 'Download Code from GitHub'
          echo '**************************'
          //git branch: 'master',
          //    credentialsId: '36f2ed2c-cd54-4bb0-a977-044253450d8c',
          //    url: 'https://github.com/autousers/Webapp-api.git'
          //sh 'ls -l'
        }
      }
        stage('Coverity Scan') {
          agent {
              node {
                  label 'covanly-linux'
              }
          }
          steps {
            echo 'test Coverity'
          }
        }
        stage('BuildImage') {
          agent {
              node {
                  label 'covanly-linux'
              }
          }
          steps {
            echo 'Build Docker Image'
            echo '***************************'
            //sh 'docker build -t webapi:pipeline /home/jenkins/workspace/WebAPI/'
            //sh 'docker images'
          }
        }
        stage('Blackduck Scan') {
          agent {
              node {
                  label 'covanly-linux'
              }
          }
          steps {
            echo 'Blackduck scan test'
          }
        }
    }
}
