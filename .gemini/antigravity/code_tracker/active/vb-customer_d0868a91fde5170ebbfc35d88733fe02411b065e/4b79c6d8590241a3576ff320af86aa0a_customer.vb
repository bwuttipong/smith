ýImports WMS_STD_Formula
Imports WMS_STD_Formula.W_Module
Public Class customer : Inherits DBType_SQLServer
    ' Fields
    Private _dataTable As DataTable = New DataTable
    Public ReadOnly Property DataTable() As DataTable
        Get
            Return _dataTable
        End Get
    End Property
    Public Sub ShowData(ByVal ColumnName As String, ByVal pFilterValue As String)
        Dim strSQL As String = ""
        Dim strWhere As String = ""
        Try
            strSQL = "SELECT ms_Customer.*, ms_Customer_Type.Customer_Type_Name, ms_Status.Status_Name FROM ms_Customer INNER JOIN ms_Customer_Type ON ms_Customer.Customer_Type_Id = ms_Customer_Type.Customer_Type_Id INNER JOIN ms_Status ON ms_Customer.Status = ms_Status.Status"
            'strSQL = "SELECT ms_Customer.Customer_Id, ms_Customer.Customer_Name, ms_Customer.Customer_Addr,ms_Customer.Start_Date, "
            'strSQL &= "ms_Customer.End_date,ms_Customer_Type.Customer_Type_Name, ms_Status.Status_Name"
            'strSQL &= "FROM ms_Customer "
            'strSQL &= "INNER JOIN ms_Customer_Type ON ms_Customer.Customer_Type_Id = ms_Customer_Type.Customer_Type_Id "
            'strSQL &= "INNER JOIN ms_Status ON ms_Customer.Customer_Id = ms_Status.Status"
            strWhere = ""
            If Not pFilterValue = "" Then
                strWhere = pFilterValue
            End If

            SetSQLString = strSQL + strWhere
            connectDB()
            EXEC_DataAdapter()
            _dataTable = GetDataTable
        Catch ex As Exception
            Throw ex
        Finally
            disconnectDB()
        End Try
    End Sub
    Public Sub GetIndex()
        Dim strSQL As String
        Try
            strSQL = "SELECT TOP 1 Customer_Id FROM ms_Customer ORDER BY Customer_Id DESC"
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
ý"(d0868a91fde5170ebbfc35d88733fe02411b065e2Jfile:///Users/Jeff/Workspaces/vb-customer/Customer/ms_Customer/customer.vb:)file:///Users/Jeff/Workspaces/vb-customer