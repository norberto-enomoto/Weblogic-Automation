# 
# WebLogic Automation Book Source Code (WLST script collection)
# 
# This file is part of the WLS-Automation book sourcecode software distribution. 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
# @author Martin Heinzl
# Copyright (C) 2013 MH-EnterpriseConsulting, All rights reserved.
#
#
#

###########################################################################
# Create a datasource with wallets and gridlink feature
###########################################################################

import sys



###################################################################
# create datasource
###################################################################
def createDatasource(datasource_name,datasource_jndiname, datasource_WalletDir, datasource_url, datasource_onsnodes):
            try:
                cd('/')
                allClusters = cmo.getClusters()

                print ''
                print 'Creating DataSource: ',datasource_name,' ....'
                cmo.createJDBCSystemResource(datasource_name)
                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name)
                cmo.setName(datasource_name)

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCDataSourceParams/' + datasource_name )
                set('JNDINames',jarray.array([String(datasource_jndiname)], String))

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCDriverParams/' + datasource_name )
                cmo.setUrl(datasource_url)
                cmo.setDriverName( 'oracle.jdbc.OracleDriver' );

                # Except Wallet => User/Passwort implementtation deleted from script

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCConnectionPoolParams/' + datasource_name )
                cmo.setTestTableName('SQL SELECT * FROM DUAL');

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCDriverParams/' + datasource_name + '/Properties/' + datasource_name )
                cmo.createProperty('oracle.net.wallet_location')

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCDriverParams/' + datasource_name + '/Properties/' + datasource_name + '/Properties/oracle.net.wallet_location')
                cmo.setValue(datasource_WalletDir);

                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCDataSourceParams/' + datasource_name )
                cmo.setGlobalTransactionsProtocol('None');

                cd('/SystemResources/' + datasource_name );
                set('Targets',allClusters)

                print '    DataSource: ',datasource_name,', will be changed to GridLink !!!'
                cd('/JDBCSystemResources/' + datasource_name + '/JDBCResource/' + datasource_name + '/JDBCOracleParams/' + datasource_name)
                cmo.setFanEnabled(true)
                cmo.setOnsNodeList(datasource_onsnodes)
                
                
                
                print 'DataSource: ',datasource_name,', has been created Successfully !!!'

            except:
                dumpStack();
                print '***** CANNOT CREATE DATASOURCE !!! Check If the DataSource With the Name : ' , datasource_name ,' Alreday exists or NOT...'
                print ''

                
# ================================================================
#           Main Code Execution
# ================================================================
if __name__== "main":
        print 'Create a datasource with wallets and gridlink feature';
        print '#';
        print '';

        connect('weblogic','< password >','t3://test-wlsautomation.de:7001')
        edit()
        startEdit()

        createDatasource('TestDatasource','jdbc/myDS', '/files/wallets/testwallet', 'jdbc:oracle:thin:/@testserver.db.wlsautomation.de:1521:ORCL','testserver_1.db.wlsautomation.de:6200,testserver_2.db.wlsautomation.de:6200')
        
        save()
        activate()

