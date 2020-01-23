pipeline {
    agent any
    environment {
        def PROJECTS_AVAIL = ["streaming-api-client", "rest-api-python-scripts"]
        def runtests = []
        def testresults = []
    }
    stages {
        stage('Build'){
            steps {
                sh 'python --version'
                sh 'git fetch'
                script {
                    commitChangeset = sh(returnStdout: true, script: 'git diff-tree --no-commit-id --name-status -r HEAD').trim()
                    for (int i = 0; i < env.PROJECTS_AVAIL.size(); i++) {
                        if (commitChangeset.contains(env.PROJECTS_AVAIL[i])) {
                            env.runtests.add(env.PROJECTS_AVAIL[i])
                        }
                    }
                    println("ChangeSets are:")
                    if (env.runtests.contains("streaming-api-client")) {
                        println("Has streaming-api-client changes!")
                    }
                    if (env.runtests.contains("rest-api-python-scripts")) {
                        println("Has rest-api-python-scripts changes!")
                    }
                }
            }
        }
        stage('Test') {
            steps { 
                sh 'ls' 
            }
        }
    }
}
