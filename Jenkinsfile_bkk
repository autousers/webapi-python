pipeline {
    agent none
    stages {
        stage('Coverity Scan') {
          agent {
              node {
                  label 'covanly-linux'
              }
          }
          steps {
            echo 'test Coverity'
            withCoverityEnvironment(coverityInstanceUrl: 'http://10.103.3.36:8080', createMissingProjectsAndStreams: true, projectName: 'webapp-test', streamName: 'webapp-test', viewName: 'High Impact Outstanding') {
              sh """
                cov-capture --dir idir --source-dir .
                cov-analyze --dir idir --all --webapp-security --distrust-all --strip-path $WORKSPACE
                cov-commit-defects --dir idir --url $COV_URL --stream $COV_STREAM --auth-key-file $COV_AUTH_KEY_PATH
              """
            }
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
            sh """
              docker build -t autousers/mywebapi:test $WORKSPACE
              docker images
              docker push autousers/mywebapi:test
            """
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
            synopsys_detect detectProperties: """--blackduck.url=https://nforcesecure.app.blackduck.com \\
                --detect.project.name=webapp-test \\
                --detect.project.version.name=1.0 \\
                --detect.target.type=IMAGE \\
                --detect.tools.excluded=BINARY_SCAN \\
                --detect.docker.image=autousers/mywebapi:test""", downloadStrategyOverride: [$class: 'ScriptOrJarDownloadStrategy']
          }
        }
        stage('Prisma Image Scan') {
          agent {
            node {
              label 'covanly-linux'
            }
          }
          steps {
            // Scan the image
            prismaCloudScanImage ca: '',
            cert: '',
            dockerAddress: 'unix:///var/run/docker.sock',
            image: 'autousers/mywebapi*',
            key: '',
            logLevel: 'info',
            podmanPath: '',
            project: '',
            resultsFile: 'prisma-cloud-scan-results.json',
            ignoreImageBuildTime:true
          }
        }
      }
      post {
        always {
          // The post section lets you run the publish step regardless of the scan results
          prismaCloudPublish resultsFilePattern: 'prisma-cloud-scan-results.json'
        }
      }
}
