'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/api';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface BudgetSummary {
  total_budget: number;
  total_spent: number;
  remaining: number;
  budget_count: number;
}

interface CategorySpending {
  category: string;
  amount: number;
  budget: number;
  percentage: number;
}

interface Expense {
  id: number;
  amount: number;
  date: string;
  description: string;
  category_id: number;
}

interface Category {
  id: number;
  name: string;
}

export default function DashboardPage() {
  const [budgetSummary, setBudgetSummary] = useState<BudgetSummary | null>(null);
  const [categorySpending, setCategorySpending] = useState<CategorySpending[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444'];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [budgetRes, expensesRes, categoriesRes] = await Promise.all([
        api.get('/budgets/summary'),
        api.get('/expenses/'),
        api.get('/categories/'),
      ]);

      const budgetData = budgetRes.data;
      const expensesData = expensesRes.data;
      const categoriesData = categoriesRes.data;

      setExpenses(expensesData);
      setCategories(categoriesData);

      if (Array.isArray(budgetData) && budgetData.length > 0) {
        const summary = {
          total_budget: budgetData.reduce((sum: number, item: any) => sum + item.budget, 0),
          total_spent: budgetData.reduce((sum: number, item: any) => sum + item.spent, 0),
          remaining: budgetData.reduce((sum: number, item: any) => sum + item.remaining, 0),
          budget_count: budgetData.length,
        };
        setBudgetSummary(summary);

        // Prepare category spending data
        const categoryData = budgetData.map((item: any) => ({
          category: item.category,
          amount: item.spent,
          budget: item.budget,
          percentage: item.budget > 0 ? (item.spent / item.budget) * 100 : 0,
        }));
        setCategorySpending(categoryData);
      } else {
        // Fallback: Calculate from expenses and categories directly
        // Get all budgets
        const budgetsRes = await api.get('/budgets/');
        const budgets = budgetsRes.data;

        if (budgets && budgets.length > 0) {
          // Calculate spending per category
          const categorySpendingMap = new Map();

          expensesData.forEach((expense: any) => {
            const current = categorySpendingMap.get(expense.category_id) || 0;
            categorySpendingMap.set(expense.category_id, current + expense.amount);
          });

          const totalBudget = budgets.reduce((sum: number, b: any) => sum + b.amount, 0);
          const totalSpent = expensesData.reduce((sum: number, e: any) => sum + e.amount, 0);

          setBudgetSummary({
            total_budget: totalBudget,
            total_spent: totalSpent,
            remaining: totalBudget - totalSpent,
            budget_count: budgets.length,
          });

          // Prepare category spending data
          const categoryData = budgets.map((budget: any) => {
            const category = categoriesData.find((c: any) => c.id === budget.category_id);
            const spent = categorySpendingMap.get(budget.category_id) || 0;
            return {
              category: category?.name || 'Unknown',
              amount: spent,
              budget: budget.amount,
              percentage: budget.amount > 0 ? (spent / budget.amount) * 100 : 0,
            };
          });
          setCategorySpending(categoryData);
        }
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Process expenses by date for trend chart
  const getExpenseTrend = () => {
    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - i));
      return date.toISOString().split('T')[0];
    });

    return last7Days.map((date) => {
      const dayExpenses = expenses.filter((exp) => exp.date.startsWith(date));
      const total = dayExpenses.reduce((sum, exp) => sum + exp.amount, 0);
      return {
        date: new Date(date).toLocaleDateString('en-US', { weekday: 'short' }),
        amount: total,
      };
    });
  };

  // Get recent expenses
  const getRecentExpenses = () => {
    return [...expenses]
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      .slice(0, 5);
  };

  const getCategoryName = (categoryId: number) => {
    return categories.find((c) => c.id === categoryId)?.name || 'Unknown';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  const expenseTrend = getExpenseTrend();
  const recentExpenses = getRecentExpenses();
  const budgetPercentage = budgetSummary && budgetSummary.total_budget > 0
    ? (budgetSummary.total_spent / budgetSummary.total_budget) * 100
    : 0;

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Welcome Section with Stats */}
      <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-xl shadow-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">Financial Overview</h2>
        <p className="text-indigo-100">Your complete spending analytics at a glance</p>
      </div>

      {budgetSummary && budgetSummary.budget_count > 0 ? (
        <>
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Total Budget</p>
                  <p className="text-3xl font-bold text-gray-900">${budgetSummary.total_budget.toFixed(2)}</p>
                </div>
                <div className="bg-blue-100 rounded-full p-3">
                  <svg className="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-red-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Total Spent</p>
                  <p className="text-3xl font-bold text-gray-900">${budgetSummary.total_spent.toFixed(2)}</p>
                  <p className="text-xs text-gray-500 mt-1">{budgetPercentage.toFixed(1)}% of budget</p>
                </div>
                <div className="bg-red-100 rounded-full p-3">
                  <svg className="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Remaining</p>
                  <p className="text-3xl font-bold text-gray-900">${budgetSummary.remaining.toFixed(2)}</p>
                  <p className="text-xs text-gray-500 mt-1">{(100 - budgetPercentage).toFixed(1)}% left</p>
                </div>
                <div className="bg-green-100 rounded-full p-3">
                  <svg className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Categories</p>
                  <p className="text-3xl font-bold text-gray-900">{budgetSummary.budget_count}</p>
                  <p className="text-xs text-gray-500 mt-1">{expenses.length} transactions</p>
                </div>
                <div className="bg-purple-100 rounded-full p-3">
                  <svg className="h-8 w-8 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Spending Trend Line Chart */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">7-Day Spending Trend</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={expenseTrend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="date" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                    formatter={(value: any) => `$${value.toFixed(2)}`}
                  />
                  <Line type="monotone" dataKey="amount" stroke="#6366f1" strokeWidth={3} dot={{ fill: '#6366f1', r: 5 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Category Spending Pie Chart */}
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Spending by Category</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={categorySpending}
                    dataKey="amount"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label={(entry) => `${entry.category}: $${entry.amount.toFixed(0)}`}
                  >
                    {categorySpending.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: any) => `$${value.toFixed(2)}`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Budget vs Spent Bar Chart */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Budget vs Actual Spending</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categorySpending}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="category" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                  formatter={(value: any) => `$${value.toFixed(2)}`}
                />
                <Legend />
                <Bar dataKey="budget" fill="#10b981" name="Budget" radius={[8, 8, 0, 0]} />
                <Bar dataKey="amount" fill="#ef4444" name="Spent" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Recent Transactions */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Recent Transactions</h3>
              <Link href="/dashboard/expenses" className="text-sm text-indigo-600 hover:text-indigo-800 font-medium">
                View all →
              </Link>
            </div>
            {recentExpenses.length > 0 ? (
              <div className="space-y-3">
                {recentExpenses.map((expense) => (
                  <div key={expense.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <div className="flex items-center space-x-4">
                      <div className="bg-indigo-100 rounded-full p-2">
                        <svg className="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                        </svg>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{expense.description}</p>
                        <p className="text-sm text-gray-500">{getCategoryName(expense.category_id)} • {new Date(expense.date).toLocaleDateString()}</p>
                      </div>
                    </div>
                    <p className="text-lg font-bold text-gray-900">${expense.amount.toFixed(2)}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No transactions yet</p>
            )}
          </div>
        </>
      ) : (
        <div className="bg-yellow-50 border-2 border-yellow-200 rounded-xl p-8 text-center">
          <svg className="h-16 w-16 text-yellow-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Started</h3>
          <p className="text-gray-600 mb-6">
            Create categories and budgets to start tracking your expenses and see beautiful analytics!
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/dashboard/categories" className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium">
              Create Categories
            </Link>
            <Link href="/dashboard/budgets" className="px-6 py-3 bg-white text-indigo-600 border-2 border-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors font-medium">
              Set Budgets
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
