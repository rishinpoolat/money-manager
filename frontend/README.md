# Money Manager Frontend

This is the frontend application for the Money Manager project, built with Next.js, TypeScript, and TailwindCSS.

## Features

- **Authentication**: Login and Registration pages with JWT token-based authentication
- **Dashboard**: Overview of your budget summary with key metrics
- **Responsive Design**: Mobile-friendly interface with TailwindCSS
- **Type Safety**: Built with TypeScript for better development experience

## Pages

- `/` - Home page (redirects to login)
- `/login` - User login page
- `/register` - User registration page
- `/dashboard` - Main dashboard with budget summary and quick actions

## Getting Started

### Prerequisites

Make sure the backend FastAPI server is running on `http://localhost:8000`

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Build for Production

```bash
npm run build
npm start
```

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **HTTP Client**: Fetch API
- **State Management**: React Hooks (useState, useEffect)

## Project Structure

```
frontend/
├── app/
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── register/
│   │   └── page.tsx        # Register page
│   ├── dashboard/
│   │   └── page.tsx        # Dashboard page
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   └── globals.css         # Global styles
├── public/                 # Static assets
└── package.json
```

## API Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000` with the following endpoints:

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/users/me` - Get current user info
- `GET /api/budgets/summary` - Get budget summary
