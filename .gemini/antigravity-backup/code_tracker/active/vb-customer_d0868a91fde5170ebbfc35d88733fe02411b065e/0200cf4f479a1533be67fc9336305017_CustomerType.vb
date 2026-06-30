§Imports WMS_STD_Formula
Imports WMS_STD_Formula.W_Module
Public Class CustomerType : Inherits DBType_SQLServer
    Private _dataTable As DataTable = New DataTable
    Public ReadOnly Property DataTable() As DataTable
        Get
            Return _dataTable
        End Get
    End Property
    Public Sub getCustomerType()
        Dim strSQL As String = ""

        Try
            strSQL = "SELECT * FROM ms_Customer_Type"
            SetSQLString = strSQL
            connectDB()
            EXEC_DataAdapter()
            _dataTable = GetDataTable
        Catch ex As Exception
            Throw ex
        Finally
            disconnectDB()
        End Try
    End Sub

    Public Sub getCustomerStatus()
        Dim strSQL As String = ""
        Try
            strSQL = "SELECT * FROM ms_Status"
            SetSQLString = strSQL
            connectDB()
            EXEC_DataAdapter()
            _dataTable = GetDataTable
        Catch ex As Exception
            Throw ex
        Finally
            disconnectDB()
        End Try
    End Sub
End Class
§"(d0868a91fde5170ebbfc35d88733fe02411b065e2Nfile:///Users/Jeff/Workspaces/vb-customer/Customer/ms_Customer/CustomerType.vb:)file:///Users/Jeff/Workspaces/vb-customer