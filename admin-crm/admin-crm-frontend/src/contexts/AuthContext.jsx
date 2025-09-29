import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const API_BASE_URL = 'http://localhost:5011/api'

  // Check if user is authenticated on app load
  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/me`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const result = await response.json()
        if (result.success) {
          setUser(result.user)
          setIsAuthenticated(true)
        }
      }
    } catch (error) {
      console.error('Auth check failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (username, password, rememberMe = false) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          remember_me: rememberMe,
        }),
      })

      const result = await response.json()

      if (result.success) {
        setUser(result.user)
        setIsAuthenticated(true)
        return { success: true, user: result.user }
      } else {
        return { success: false, message: result.message }
      }
    } catch (error) {
      console.error('Login failed:', error)
      return { success: false, message: 'Login failed. Please try again.' }
    }
  }

  const logout = async () => {
    try {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      setUser(null)
      setIsAuthenticated(false)
    }
  }

  const changePassword = async (currentPassword, newPassword) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/change-password`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      })

      const result = await response.json()
      return result
    } catch (error) {
      console.error('Password change failed:', error)
      return { success: false, message: 'Password change failed. Please try again.' }
    }
  }

  const hasPermission = (permission) => {
    if (!user) return false
    
    const permissions = {
      'super_admin': [
        'view_dashboard', 'manage_users', 'manage_sellers', 'manage_orders', 
        'manage_products', 'view_analytics', 'create_admin', 'create_moderator',
        'delete_users', 'system_config', 'audit_logs'
      ],
      'admin': [
        'view_dashboard', 'manage_users', 'manage_sellers', 'manage_orders',
        'manage_products', 'view_analytics', 'create_moderator', 'delete_moderator'
      ],
      'moderator': [
        'view_dashboard', 'view_users', 'manage_orders', 'view_products'
      ]
    }
    
    return permissions[user.role]?.includes(permission) || false
  }

  const canManageUsers = () => {
    return hasPermission('manage_users')
  }

  const canCreateModerator = () => {
    return hasPermission('create_moderator')
  }

  const canCreateAdmin = () => {
    return hasPermission('create_admin')
  }

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    changePassword,
    hasPermission,
    canManageUsers,
    canCreateModerator,
    canCreateAdmin,
    checkAuthStatus,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

