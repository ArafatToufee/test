import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'
import { 
  BarChart3, 
  Users, 
  Store, 
  ShoppingCart, 
  Package, 
  TrendingUp, 
  Search,
  LogOut,
  Settings,
  Shield,
  UserPlus
} from 'lucide-react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import UserManagement from './components/UserManagement'
import './App.css'

const API_BASE_URL = 'http://localhost:5011/api'

function AppContent() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [dashboardData, setDashboardData] = useState(null)
  const [users, setUsers] = useState([])
  const [sellers, setSellers] = useState([])
  const [orders, setOrders] = useState([])
  const [products, setProducts] = useState([])
  const [revenueData, setRevenueData] = useState([])
  const [userGrowthData, setUserGrowthData] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')

  const { user, logout, hasPermission } = useAuth()

  useEffect(() => {
    if (activeTab === 'dashboard') {
      fetchDashboardData()
      fetchAnalytics()
    } else if (activeTab === 'users' && hasPermission('view_users')) {
      fetchUsers()
    } else if (activeTab === 'sellers' && hasPermission('manage_sellers')) {
      fetchSellers()
    } else if (activeTab === 'orders' && hasPermission('manage_orders')) {
      fetchOrders()
    } else if (activeTab === 'products' && hasPermission('view_products')) {
      fetchProducts()
    }
  }, [activeTab])

  const fetchWithAuth = async (url, options = {}) => {
    return fetch(url, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })
  }

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/dashboard`)
      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setDashboardData(result.data)
        }
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAnalytics = async () => {
    try {
      const [revenueResponse, userResponse] = await Promise.all([
        fetchWithAuth(`${API_BASE_URL}/admin/analytics/revenue`),
        fetchWithAuth(`${API_BASE_URL}/admin/analytics/users`)
      ])

      if (revenueResponse.ok) {
        const revenueResult = await revenueResponse.json()
        if (revenueResult.success) {
          const formattedData = revenueResult.data.months.map((month, index) => ({
            month,
            revenue: revenueResult.data.revenue[index]
          }))
          setRevenueData(formattedData)
        }
      }

      if (userResponse.ok) {
        const userResult = await userResponse.json()
        if (userResult.success) {
          const formattedData = userResult.data.months.map((month, index) => ({
            month,
            users: userResult.data.new_users[index]
          }))
          setUserGrowthData(formattedData)
        }
      }
    } catch (error) {
      console.error('Error fetching analytics:', error)
    }
  }

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/users?search=${searchTerm}`)
      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setUsers(result.data.users)
        }
      }
    } catch (error) {
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchSellers = async () => {
    try {
      setLoading(true)
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/sellers?search=${searchTerm}`)
      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setSellers(result.data.sellers)
        }
      }
    } catch (error) {
      console.error('Error fetching sellers:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchOrders = async () => {
    try {
      setLoading(true)
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/orders?status=${statusFilter}`)
      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setOrders(result.data.orders)
        }
      }
    } catch (error) {
      console.error('Error fetching orders:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/products?category=${categoryFilter}`)
      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setProducts(result.data.products)
        }
      }
    } catch (error) {
      console.error('Error fetching products:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateUserStatus = async (userId, status) => {
    try {
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/users/${userId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status })
      })
      if (response.ok) {
        fetchUsers()
      }
    } catch (error) {
      console.error('Error updating user status:', error)
    }
  }

  const updateSellerStatus = async (sellerId, status) => {
    try {
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/sellers/${sellerId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status })
      })
      if (response.ok) {
        fetchSellers()
      }
    } catch (error) {
      console.error('Error updating seller status:', error)
    }
  }

  const updateOrderStatus = async (orderId, status) => {
    try {
      const response = await fetchWithAuth(`${API_BASE_URL}/admin/orders/${orderId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status })
      })
      if (response.ok) {
        fetchOrders()
      }
    } catch (error) {
      console.error('Error updating order status:', error)
    }
  }

  const handleLogout = async () => {
    await logout()
  }

  const renderDashboard = () => (
    <ProtectedRoute requiredPermission="view_dashboard">
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Overview of your e-commerce platform performance
          </p>
        </div>

        {dashboardData && (
          <>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Users</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.total_users?.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    +{dashboardData.active_users_today} active today
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${dashboardData.total_revenue?.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    +{dashboardData.monthly_growth}% from last month
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Orders</CardTitle>
                  <ShoppingCart className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.total_orders?.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    {dashboardData.pending_orders} pending
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Sellers</CardTitle>
                  <Store className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dashboardData.total_sellers?.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    {dashboardData.refund_requests} refund requests
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Revenue Overview</CardTitle>
                  <CardDescription>Monthly revenue for the last 12 months</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={revenueData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']} />
                      <Bar dataKey="revenue" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>User Growth</CardTitle>
                  <CardDescription>New user registrations per month</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={userGrowthData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [value.toLocaleString(), 'New Users']} />
                      <Line type="monotone" dataKey="users" stroke="#82ca9d" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </>
        )}
      </div>
    </ProtectedRoute>
  )

  const renderUsers = () => (
    <ProtectedRoute requiredPermission="view_users">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Users</h2>
            <p className="text-muted-foreground">Manage platform users</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search users..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 w-64"
              />
            </div>
            <Button onClick={fetchUsers}>Search</Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Registration Date</TableHead>
                  <TableHead>Total Orders</TableHead>
                  <TableHead>Total Spent</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell className="font-medium">{user.name}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      <Badge variant={user.status === 'active' ? 'default' : 'secondary'}>
                        {user.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{user.registration_date}</TableCell>
                    <TableCell>{user.total_orders}</TableCell>
                    <TableCell>${user.total_spent}</TableCell>
                    <TableCell>
                      {hasPermission('manage_users') && (
                        <Select
                          value={user.status}
                          onValueChange={(value) => updateUserStatus(user.id, value)}
                        >
                          <SelectTrigger className="w-32">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="active">Active</SelectItem>
                            <SelectItem value="inactive">Inactive</SelectItem>
                            <SelectItem value="suspended">Suspended</SelectItem>
                          </SelectContent>
                        </Select>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  )

  const renderSellers = () => (
    <ProtectedRoute requiredPermission="manage_sellers">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Sellers</h2>
            <p className="text-muted-foreground">Manage platform sellers</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search sellers..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 w-64"
              />
            </div>
            <Button onClick={fetchSellers}>Search</Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Registration Date</TableHead>
                  <TableHead>Products</TableHead>
                  <TableHead>Total Sales</TableHead>
                  <TableHead>Commission Rate</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sellers.map((seller) => (
                  <TableRow key={seller.id}>
                    <TableCell className="font-medium">{seller.name}</TableCell>
                    <TableCell>{seller.email}</TableCell>
                    <TableCell>
                      <Badge variant={seller.status === 'active' ? 'default' : 'secondary'}>
                        {seller.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{seller.registration_date}</TableCell>
                    <TableCell>{seller.total_products}</TableCell>
                    <TableCell>${seller.total_sales}</TableCell>
                    <TableCell>{seller.commission_rate}%</TableCell>
                    <TableCell>
                      <Select
                        value={seller.status}
                        onValueChange={(value) => updateSellerStatus(seller.id, value)}
                      >
                        <SelectTrigger className="w-32">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="active">Active</SelectItem>
                          <SelectItem value="pending">Pending</SelectItem>
                          <SelectItem value="suspended">Suspended</SelectItem>
                        </SelectContent>
                      </Select>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  )

  const renderOrders = () => (
    <ProtectedRoute requiredPermission="manage_orders">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Orders</h2>
            <p className="text-muted-foreground">Manage platform orders</p>
          </div>
          <div className="flex items-center space-x-2">
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Statuses</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="processing">Processing</SelectItem>
                <SelectItem value="shipped">Shipped</SelectItem>
                <SelectItem value="delivered">Delivered</SelectItem>
                <SelectItem value="cancelled">Cancelled</SelectItem>
                <SelectItem value="refunded">Refunded</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={fetchOrders}>Filter</Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order ID</TableHead>
                  <TableHead>Customer</TableHead>
                  <TableHead>Seller</TableHead>
                  <TableHead>Amount</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Order Date</TableHead>
                  <TableHead>Items</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {orders.map((order) => (
                  <TableRow key={order.id}>
                    <TableCell className="font-medium">{order.id}</TableCell>
                    <TableCell>{order.customer_name}</TableCell>
                    <TableCell>{order.seller_name}</TableCell>
                    <TableCell>${order.amount}</TableCell>
                    <TableCell>
                      <Badge variant={order.status === 'delivered' ? 'default' : 'secondary'}>
                        {order.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{order.order_date}</TableCell>
                    <TableCell>{order.items_count}</TableCell>
                    <TableCell>
                      <Select
                        value={order.status}
                        onValueChange={(value) => updateOrderStatus(order.id, value)}
                      >
                        <SelectTrigger className="w-32">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="pending">Pending</SelectItem>
                          <SelectItem value="processing">Processing</SelectItem>
                          <SelectItem value="shipped">Shipped</SelectItem>
                          <SelectItem value="delivered">Delivered</SelectItem>
                          <SelectItem value="cancelled">Cancelled</SelectItem>
                          <SelectItem value="refunded">Refunded</SelectItem>
                        </SelectContent>
                      </Select>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  )

  const renderProducts = () => (
    <ProtectedRoute requiredPermission="view_products">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Products</h2>
            <p className="text-muted-foreground">Manage platform products</p>
          </div>
          <div className="flex items-center space-x-2">
            <Select value={categoryFilter} onValueChange={setCategoryFilter}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">All Categories</SelectItem>
                <SelectItem value="Electronics">Electronics</SelectItem>
                <SelectItem value="Clothing">Clothing</SelectItem>
                <SelectItem value="Home & Garden">Home & Garden</SelectItem>
                <SelectItem value="Sports">Sports</SelectItem>
                <SelectItem value="Books">Books</SelectItem>
                <SelectItem value="Beauty">Beauty</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={fetchProducts}>Filter</Button>
          </div>
        </div>

        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product Name</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Seller</TableHead>
                  <TableHead>Price</TableHead>
                  <TableHead>Stock</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {products.map((product) => (
                  <TableRow key={product.id}>
                    <TableCell className="font-medium">{product.name}</TableCell>
                    <TableCell>{product.category}</TableCell>
                    <TableCell>{product.seller_name}</TableCell>
                    <TableCell>${product.price}</TableCell>
                    <TableCell>{product.stock}</TableCell>
                    <TableCell>
                      <Badge variant={product.status === 'active' ? 'default' : 'secondary'}>
                        {product.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{product.created_date}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  )

  const renderAnalytics = () => (
    <ProtectedRoute requiredPermission="view_analytics">
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Analytics</h2>
          <p className="text-muted-foreground">
            Detailed analytics and reporting
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Revenue Overview</CardTitle>
              <CardDescription>Monthly revenue for the last 12 months</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']} />
                  <Bar dataKey="revenue" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>User Growth</CardTitle>
              <CardDescription>New user registrations per month</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={userGrowthData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(value) => [value.toLocaleString(), 'New Users']} />
                  <Line type="monotone" dataKey="users" stroke="#82ca9d" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      </div>
    </ProtectedRoute>
  )

  const renderUserManagement = () => (
    <ProtectedRoute requiredPermission="manage_users">
      <UserManagement />
    </ProtectedRoute>
  )

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return renderDashboard()
      case 'users':
        return renderUsers()
      case 'sellers':
        return renderSellers()
      case 'orders':
        return renderOrders()
      case 'products':
        return renderProducts()
      case 'analytics':
        return renderAnalytics()
      case 'user-management':
        return renderUserManagement()
      default:
        return renderDashboard()
    }
  }

  return (
    <ProtectedRoute>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-md">
          <div className="p-6">
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">RefCommerce Admin CRM</span>
            </div>
          </div>
          
          <nav className="mt-6">
            <div className="px-6 py-2">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                Main
              </p>
            </div>
            
            <Button
              variant={activeTab === 'dashboard' ? 'secondary' : 'ghost'}
              className="w-full justify-start px-6 py-3"
              onClick={() => setActiveTab('dashboard')}
            >
              <BarChart3 className="mr-3 h-4 w-4" />
              Dashboard
            </Button>
            
            {hasPermission('view_users') && (
              <Button
                variant={activeTab === 'users' ? 'secondary' : 'ghost'}
                className="w-full justify-start px-6 py-3"
                onClick={() => setActiveTab('users')}
              >
                <Users className="mr-3 h-4 w-4" />
                Users
              </Button>
            )}
            
            {hasPermission('manage_sellers') && (
              <Button
                variant={activeTab === 'sellers' ? 'secondary' : 'ghost'}
                className="w-full justify-start px-6 py-3"
                onClick={() => setActiveTab('sellers')}
              >
                <Store className="mr-3 h-4 w-4" />
                Sellers
              </Button>
            )}
            
            {hasPermission('manage_orders') && (
              <Button
                variant={activeTab === 'orders' ? 'secondary' : 'ghost'}
                className="w-full justify-start px-6 py-3"
                onClick={() => setActiveTab('orders')}
              >
                <ShoppingCart className="mr-3 h-4 w-4" />
                Orders
              </Button>
            )}
            
            {hasPermission('view_products') && (
              <Button
                variant={activeTab === 'products' ? 'secondary' : 'ghost'}
                className="w-full justify-start px-6 py-3"
                onClick={() => setActiveTab('products')}
              >
                <Package className="mr-3 h-4 w-4" />
                Products
              </Button>
            )}
            
            {hasPermission('view_analytics') && (
              <Button
                variant={activeTab === 'analytics' ? 'secondary' : 'ghost'}
                className="w-full justify-start px-6 py-3"
                onClick={() => setActiveTab('analytics')}
              >
                <TrendingUp className="mr-3 h-4 w-4" />
                Analytics
              </Button>
            )}

            {hasPermission('manage_users') && (
              <>
                <div className="px-6 py-2 mt-6">
                  <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                    Administration
                  </p>
                </div>
                
                <Button
                  variant={activeTab === 'user-management' ? 'secondary' : 'ghost'}
                  className="w-full justify-start px-6 py-3"
                  onClick={() => setActiveTab('user-management')}
                >
                  <Shield className="mr-3 h-4 w-4" />
                  User Management
                </Button>
              </>
            )}
          </nav>

          {/* User info and logout */}
          <div className="absolute bottom-0 w-64 p-4 border-t">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">
                    {user?.username?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-medium">{user?.username}</p>
                  <p className="text-xs text-muted-foreground">{user?.role?.replace('_', ' ')}</p>
                </div>
              </div>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 overflow-auto">
          <div className="p-8">
            {renderContent()}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

