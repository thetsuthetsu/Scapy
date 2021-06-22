pipeline {
    agent any
    stages {
        stage('PWD') {
            steps {
                sh 'pwd'
            }
        }
        stage('LS') {
            steps {
                sh 'ls -l'
            }
        }
        stage('DETECT') {
            steps {
                synopsys_detect detectProperties: '--blackduck.url=https://192.168.150.213 --blackduck.username=sysadmin --blackduck.password=blackduck --blackduck.trust.cert=true', downloadStrategyOverride: [$class: 'ScriptOrJarDownloadStrategy']
            }
        }
    }
    post {
        always {
            sendMail(currentBuild.currentResult)
        }
    }
}


// メールをGmailに送信する
def sendMail(result) {
    mail to: "thetsuthetsu@gmail.com",
        subject: "${env.JOB_NAME} #${env.BUILD_NUMBER} [${result}]",
        body: "Build URL: ${env.BUILD_URL}.\n\n"
}
