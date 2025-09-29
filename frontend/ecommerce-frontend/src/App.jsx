import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ShoppingCart, Search, User, Heart, Star, Plus, Minus, Camera, Mic, Brain, Shield, TrendingUp, Sparkles } from 'lucide-react'
import Chatbot from './components/Chatbot'
import './App.css'

// API Base URL
const API_BASE = 'https://8080-ipljtdvqszg3uf8p57mc6-04dbd043.manusvm.computer'

function App() {
  const [products, setProducts] = useState([])
  const [cartItems, setCartItems] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [recommendations, setRecommendations] = useState([])
  const [visualSearchResults, setVisualSearchResults] = useState([])
  const [fraudAlert, setFraudAlert] = useState(null)
  const [aiInsights, setAiInsights] = useState(null)
  const [activeTab, setActiveTab] = useState('products')

  // Sample products for demo (will be replaced with API calls)
  const sampleProducts = [
    {
      id: 'prod-1',
      name: 'Wireless Headphones',
      description: 'High-quality wireless headphones with noise cancellation',
      price: 199.99,
      category: 'Electronics',
      stock_quantity: 50,
      image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
      ai_score: 0.92,
      trending: true
    },
    {
      id: 'prod-2',
      name: 'Smartphone',
      description: 'Latest smartphone with advanced camera features',
      price: 799.99,
      category: 'Electronics',
      stock_quantity: 30,
      image_url: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
      ai_score: 0.88,
      trending: false
    },
    {
      id: 'prod-3',
      name: 'Running Shoes',
      description: 'Comfortable running shoes for all terrains',
      price: 129.99,
      category: 'Sports',
      stock_quantity: 100,
      image_url: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop',
      ai_score: 0.85,
      trending: true
    },
    {
      id: 'prod-4',
      name: 'Coffee Maker',
      description: 'Automatic coffee maker with programmable settings',
      price: 89.99,
      category: 'Home & Kitchen',
      stock_quantity: 25,
      image_url: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop',
      ai_score: 0.79,
      trending: false
    },
    {
      id: 'prod-5',
      name: 'Laptop',
      description: 'High-performance laptop for work and gaming',
      price: 1299.99,
      category: 'Electronics',
      stock_quantity: 15,
      image_url: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
      ai_score: 0.94,
      trending: true
    },
    {
      id: 'prod-6',
      name: 'Yoga Mat',
      description: 'Premium non-slip yoga mat for all exercises',
      price: 39.99,
      category: 'Sports',
      stock_quantity: 75,
      image_url: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop',
      ai_score: 0.76,
      trending: false
    }
  ]

  useEffect(() => {
    // Initialize with sample products
    setProducts(sampleProducts)
    setLoading(false)
    
    // Load AI recommendations
    loadAIRecommendations()
    
    // Load AI insights
    loadAIInsights()
  }, [])

  const loadAIRecommendations = async () => {
    try {
      // Simulate AI recommendation API call
      const mockRecommendations = sampleProducts
        .filter(p => p.ai_score > 0.8)
        .map(p => ({
          ...p,
          recommendation_reason: getRecommendationReason(p),
          confidence: p.ai_score
        }))
      
      setRecommendations(mockRecommendations.slice(0, 4))
    } catch (error) {
      console.error('Failed to load AI recommendations:', error)
    }
  }

  const loadAIInsights = async () => {
    try {
      // Simulate AI insights
      const insights = {
        trending_categories: ['Electronics', 'Sports'],
        price_predictions: {
          'Electronics': 'Prices expected to drop 5% next month',
          'Sports': 'High demand detected, prices stable'
        },
        user_behavior: 'You tend to shop for electronics on weekends',
        fraud_risk: 'Low',
        personalization_score: 0.87
      }
      
      setAiInsights(insights)
    } catch (error) {
      console.error('Failed to load AI insights:', error)
    }
  }

  const performVisualSearch = async (imageFile) => {
    try {
      // Simulate visual search API call
      const mockResults = sampleProducts
        .filter(p => Math.random() > 0.5)
        .map(p => ({
          ...p,
          visual_similarity: Math.random() * 0.4 + 0.6,
          matched_features: ['color', 'shape', 'style']
        }))
      
      setVisualSearchResults(mockResults.slice(0, 3))
      setActiveTab('visual-search')
    } catch (error) {
      console.error('Visual search failed:', error)
    }
  }

  const checkFraudRisk = async (transaction) => {
    try {
      // Simulate fraud detection API call
      const riskScore = Math.random() * 0.3 // Low risk simulation
      
      if (riskScore > 0.2) {
        setFraudAlert({
          level: 'medium',
          message: 'Unusual purchase pattern detected. Please verify your identity.',
          score: riskScore
        })
      }
    } catch (error) {
      console.error('Fraud check failed:', error)
    }
  }

  const getRecommendationReason = (product) => {
    const reasons = [
      'Based on your browsing history',
      'Trending in your area',
      'Highly rated by similar users',
      'Perfect match for your interests',
      'AI-powered recommendation'
    ]
    return reasons[Math.floor(Math.random() * reasons.length)]
  }

  const addToCart = (product) => {
    const existingItem = cartItems.find(item => item.id === product.id)
    if (existingItem) {
      setCartItems(cartItems.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setCartItems([...cartItems, { ...product, quantity: 1 }])
    }
    
    // Check fraud risk for high-value items
    if (product.price > 500) {
      checkFraudRisk({ product_id: product.id, amount: product.price })
    }
  }

  const removeFromCart = (productId) => {
    setCartItems(cartItems.filter(item => item.id !== productId))
  }

  const updateQuantity = (productId, newQuantity) => {
    if (newQuantity === 0) {
      removeFromCart(productId)
    } else {
      setCartItems(cartItems.map(item =>
        item.id === productId
          ? { ...item, quantity: newQuantity }
          : item
      ))
    }
  }

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    product.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const cartTotal = cartItems.reduce((total, item) => total + (item.price * item.quantity), 0)
  const cartItemCount = cartItems.reduce((total, item) => total + item.quantity, 0)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-blue-600 mr-2" />
              <h1 className="text-2xl font-bold text-gray-900">RefCommerce AI</h1>
            </div>

            {/* Search Bar */}
            <div className="flex-1 max-w-lg mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  type="text"
                  placeholder="Search products with AI..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full"
                />
                <Button
                  size="sm"
                  variant="ghost"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2"
                  onClick={() => document.getElementById('visual-search-input').click()}
                >
                  <Camera className="h-4 w-4" />
                </Button>
                <input
                  id="visual-search-input"
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => e.target.files[0] && performVisualSearch(e.target.files[0])}
                />
              </div>
            </div>

            {/* Navigation */}
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm">
                <Heart className="h-4 w-4 mr-2" />
                Wishlist
              </Button>
              <Button variant="ghost" size="sm" className="relative">
                <ShoppingCart className="h-4 w-4 mr-2" />
                Cart
                {cartItemCount > 0 && (
                  <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                    {cartItemCount}
                  </Badge>
                )}
              </Button>
              <Button variant="ghost" size="sm">
                <User className="h-4 w-4 mr-2" />
                Account
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Fraud Alert */}
      {fraudAlert && (
        <Alert className="mx-4 mt-4 border-orange-200 bg-orange-50">
          <Shield className="h-4 w-4" />
          <AlertDescription>
            <div className="flex items-center justify-between">
              <span>{fraudAlert.message}</span>
              <Button size="sm" variant="outline" onClick={() => setFraudAlert(null)}>
                Dismiss
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-8 mb-8 text-white">
          <div className="flex items-center mb-4">
            <Sparkles className="h-8 w-8 mr-3" />
            <h2 className="text-3xl font-bold">AI-Powered Shopping Experience</h2>
          </div>
          <p className="text-lg mb-6">Discover products with advanced AI recommendations, visual search, and fraud protection</p>
          <div className="flex space-x-4">
            <Button size="lg" variant="secondary">
              <Brain className="h-5 w-5 mr-2" />
              Get AI Recommendations
            </Button>
            <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-blue-600">
              <Camera className="h-5 w-5 mr-2" />
              Visual Search
            </Button>
          </div>
        </div>

        {/* AI Insights Panel */}
        {aiInsights && (
          <div className="bg-white rounded-lg p-6 mb-8 shadow-sm border">
            <div className="flex items-center mb-4">
              <TrendingUp className="h-6 w-6 text-green-600 mr-2" />
              <h3 className="text-xl font-semibold">AI Market Insights</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-900">Trending Categories</h4>
                <p className="text-blue-700">{aiInsights.trending_categories.join(', ')}</p>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <h4 className="font-medium text-green-900">Price Prediction</h4>
                <p className="text-green-700">{aiInsights.price_predictions.Electronics}</p>
              </div>
              <div className="p-4 bg-purple-50 rounded-lg">
                <h4 className="font-medium text-purple-900">Personalization</h4>
                <p className="text-purple-700">Score: {(aiInsights.personalization_score * 100).toFixed(0)}%</p>
              </div>
            </div>
          </div>
        )}

        {/* Tabs for different views */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="products">All Products</TabsTrigger>
            <TabsTrigger value="recommendations">AI Recommendations</TabsTrigger>
            <TabsTrigger value="visual-search">Visual Search</TabsTrigger>
            <TabsTrigger value="trending">Trending</TabsTrigger>
          </TabsList>

          <TabsContent value="products">
            {/* Categories */}
            <div className="mb-8">
              <h3 className="text-xl font-semibold mb-4">Shop by Category</h3>
              <div className="flex space-x-4 overflow-x-auto pb-2">
                {['Electronics', 'Sports', 'Home & Kitchen', 'Fashion', 'Books'].map((category) => (
                  <Badge key={category} variant="outline" className="whitespace-nowrap cursor-pointer hover:bg-gray-100">
                    {category}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Products Grid */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold">Featured Products</h3>
                <p className="text-gray-600">{filteredProducts.length} products found</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredProducts.map((product) => (
                  <Card key={product.id} className="hover:shadow-lg transition-shadow duration-200">
                    <div className="relative">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="w-full h-48 object-cover rounded-t-lg"
                      />
                      <Button
                        size="sm"
                        variant="secondary"
                        className="absolute top-2 right-2"
                      >
                        <Heart className="h-4 w-4" />
                      </Button>
                      {product.trending && (
                        <Badge className="absolute top-2 left-2 bg-red-500">
                          <TrendingUp className="h-3 w-3 mr-1" />
                          Trending
                        </Badge>
                      )}
                    </div>
                    <CardContent className="p-4">
                      <div className="flex items-center mb-2">
                        <div className="flex text-yellow-400">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="h-4 w-4 fill-current" />
                          ))}
                        </div>
                        <span className="text-sm text-gray-600 ml-2">(4.5)</span>
                        <Badge variant="outline" className="ml-auto text-xs">
                          AI: {(product.ai_score * 100).toFixed(0)}%
                        </Badge>
                      </div>
                      <h4 className="font-semibold text-lg mb-2">{product.name}</h4>
                      <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-blue-600">${product.price}</span>
                        <Badge variant="outline">{product.category}</Badge>
                      </div>
                    </CardContent>
                    <CardFooter className="p-4 pt-0">
                      <Button
                        onClick={() => addToCart(product)}
                        className="w-full"
                        disabled={product.stock_quantity === 0}
                      >
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        {product.stock_quantity === 0 ? 'Out of Stock' : 'Add to Cart'}
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="recommendations">
            <div className="mb-8">
              <div className="flex items-center mb-6">
                <Brain className="h-6 w-6 text-blue-600 mr-2" />
                <h3 className="text-xl font-semibold">AI-Powered Recommendations</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {recommendations.map((product) => (
                  <Card key={product.id} className="hover:shadow-lg transition-shadow duration-200">
                    <div className="relative">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="w-full h-48 object-cover rounded-t-lg"
                      />
                      <Badge className="absolute top-2 left-2 bg-blue-500">
                        <Brain className="h-3 w-3 mr-1" />
                        AI Pick
                      </Badge>
                    </div>
                    <CardContent className="p-4">
                      <div className="flex items-center mb-2">
                        <Badge variant="outline" className="text-xs">
                          {(product.confidence * 100).toFixed(0)}% match
                        </Badge>
                      </div>
                      <h4 className="font-semibold text-lg mb-2">{product.name}</h4>
                      <p className="text-sm text-blue-600 mb-3">{product.recommendation_reason}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-blue-600">${product.price}</span>
                      </div>
                    </CardContent>
                    <CardFooter className="p-4 pt-0">
                      <Button
                        onClick={() => addToCart(product)}
                        className="w-full"
                      >
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        Add to Cart
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>

          <TabsContent value="visual-search">
            <div className="mb-8">
              <div className="flex items-center mb-6">
                <Camera className="h-6 w-6 text-purple-600 mr-2" />
                <h3 className="text-xl font-semibold">Visual Search Results</h3>
              </div>
              
              {visualSearchResults.length === 0 ? (
                <div className="text-center py-12">
                  <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h4 className="text-lg font-medium text-gray-900 mb-2">Upload an image to search</h4>
                  <p className="text-gray-600 mb-4">Find similar products using AI-powered visual recognition</p>
                  <Button onClick={() => document.getElementById('visual-search-input').click()}>
                    <Camera className="h-4 w-4 mr-2" />
                    Upload Image
                  </Button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {visualSearchResults.map((product) => (
                    <Card key={product.id} className="hover:shadow-lg transition-shadow duration-200">
                      <div className="relative">
                        <img
                          src={product.image_url}
                          alt={product.name}
                          className="w-full h-48 object-cover rounded-t-lg"
                        />
                        <Badge className="absolute top-2 left-2 bg-purple-500">
                          {(product.visual_similarity * 100).toFixed(0)}% similar
                        </Badge>
                      </div>
                      <CardContent className="p-4">
                        <h4 className="font-semibold text-lg mb-2">{product.name}</h4>
                        <p className="text-sm text-purple-600 mb-3">
                          Matched: {product.matched_features.join(', ')}
                        </p>
                        <div className="flex items-center justify-between">
                          <span className="text-2xl font-bold text-blue-600">${product.price}</span>
                        </div>
                      </CardContent>
                      <CardFooter className="p-4 pt-0">
                        <Button
                          onClick={() => addToCart(product)}
                          className="w-full"
                        >
                          <ShoppingCart className="h-4 w-4 mr-2" />
                          Add to Cart
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="trending">
            <div className="mb-8">
              <div className="flex items-center mb-6">
                <TrendingUp className="h-6 w-6 text-green-600 mr-2" />
                <h3 className="text-xl font-semibold">AI-Detected Trending Products</h3>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {products.filter(p => p.trending).map((product) => (
                  <Card key={product.id} className="hover:shadow-lg transition-shadow duration-200">
                    <div className="relative">
                      <img
                        src={product.image_url}
                        alt={product.name}
                        className="w-full h-48 object-cover rounded-t-lg"
                      />
                      <Badge className="absolute top-2 left-2 bg-green-500">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        Hot
                      </Badge>
                    </div>
                    <CardContent className="p-4">
                      <h4 className="font-semibold text-lg mb-2">{product.name}</h4>
                      <p className="text-sm text-green-600 mb-3">High demand detected by AI</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-blue-600">${product.price}</span>
                      </div>
                    </CardContent>
                    <CardFooter className="p-4 pt-0">
                      <Button
                        onClick={() => addToCart(product)}
                        className="w-full"
                      >
                        <ShoppingCart className="h-4 w-4 mr-2" />
                        Add to Cart
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </div>
          </TabsContent>
        </Tabs>

        {/* Shopping Cart Sidebar */}
        {cartItems.length > 0 && (
          <div className="fixed right-4 top-20 w-80 bg-white rounded-lg shadow-lg border p-4 max-h-96 overflow-y-auto">
            <div className="flex items-center mb-4">
              <ShoppingCart className="h-5 w-5 mr-2" />
              <h4 className="font-semibold">Shopping Cart ({cartItemCount} items)</h4>
              {fraudAlert && (
                <Shield className="h-4 w-4 ml-auto text-orange-500" />
              )}
            </div>
            <div className="space-y-3">
              {cartItems.map((item) => (
                <div key={item.id} className="flex items-center space-x-3 p-2 border rounded">
                  <img src={item.image_url} alt={item.name} className="w-12 h-12 object-cover rounded" />
                  <div className="flex-1">
                    <h5 className="font-medium text-sm">{item.name}</h5>
                    <p className="text-blue-600 font-semibold">${item.price}</p>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      <Minus className="h-3 w-3" />
                    </Button>
                    <span className="px-2 text-sm">{item.quantity}</span>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      <Plus className="h-3 w-3" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t">
              <div className="flex justify-between items-center mb-3">
                <span className="font-semibold">Total: ${cartTotal.toFixed(2)}</span>
                <Badge variant="outline" className="text-xs">
                  <Shield className="h-3 w-3 mr-1" />
                  Fraud Protected
                </Badge>
              </div>
              <Button className="w-full">
                <Shield className="h-4 w-4 mr-2" />
                Secure Checkout
              </Button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Brain className="h-6 w-6 mr-2" />
                <h5 className="font-semibold">RefCommerce AI</h5>
              </div>
              <p className="text-gray-400">Your AI-powered shopping destination with advanced recommendations and fraud protection</p>
            </div>
            <div>
              <h5 className="font-semibold mb-4">AI Features</h5>
              <ul className="space-y-2 text-gray-400">
                <li>Smart Recommendations</li>
                <li>Visual Search</li>
                <li>Fraud Detection</li>
                <li>Price Predictions</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Customer Service</h5>
              <ul className="space-y-2 text-gray-400">
                <li>Contact Us</li>
                <li>FAQ</li>
                <li>Returns</li>
                <li>Shipping Info</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Connect</h5>
              <ul className="space-y-2 text-gray-400">
                <li>Newsletter</li>
                <li>Social Media</li>
                <li>Community</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 RefCommerce AI. All rights reserved. Powered by advanced AI technology.</p>
          </div>
        </div>
      </footer>

      {/* AI Chatbot */}
      <Chatbot />
    </div>
  )
}

export default App
