# Frontend - Hệ Thống Quản Lý KPI

React Frontend cho Hệ Thống Quản Lý KPI.

---

## 🛠️ Stack Công Nghệ

- **Framework**: React 18+
- **Build Tool**: Vite 5+
- **Language**: JavaScript (hoặc TypeScript)
- **Styling**: Tailwind CSS 3+
- **State Management**: React Context + hooks
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Forms**: React Hook Form
- **Charts**: Recharts
- **Date Handling**: date-fns

---

## 📦 Cài Đặt

### Yêu Cầu

- Node.js 18+ hoặc cao hơn
- npm hoặc yarn

### Setup

```bash
# Cài đặt dependencies
npm install

# Copy environment file (nếu cần)
cp .env.example .env
# Chỉnh sửa .env với settings của bạn

# Chạy development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🗂️ Cấu Trúc Thư Mục

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── common/         # Common components (Button, Input, etc.)
│   │   ├── kpi/            # KPI-specific components
│   │   ├── layout/         # Layout components (Header, Sidebar)
│   │   └── ...
│   │
│   ├── pages/              # Route pages
│   │   ├── Dashboard.jsx
│   │   ├── Login.jsx
│   │   ├── KPIList.jsx
│   │   ├── KPIDetail.jsx
│   │   └── ...
│   │
│   ├── services/           # API calls
│   │   ├── api.js          # Axios instance
│   │   ├── auth.js         # Authentication API
│   │   ├── kpi.js          # KPI API
│   │   └── ...
│   │
│   ├── contexts/           # React Context
│   │   ├── AuthContext.jsx
│   │   ├── NotificationContext.jsx
│   │   └── ...
│   │
│   ├── utils/              # Utility functions
│   │   ├── formatters.js
│   │   ├── validators.js
│   │   └── ...
│   │
│   ├── hooks/              # Custom hooks
│   │   ├── useAuth.js
│   │   ├── useKPI.js
│   │   └── ...
│   │
│   ├── App.jsx             # Root component
│   ├── main.jsx            # Entry point
│   └── index.css           # Global styles
│
├── public/                 # Static assets
│   ├── favicon.ico
│   ├── logo.png
│   └── ...
│
├── Dockerfile              # Docker image definition
├── nginx.conf              # Nginx configuration
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── tailwind.config.js      # Tailwind configuration
└── README.md               # This file
```

---

## 🎨 UI Components

### Layout Components
- `Header` - Navigation và user menu
- `Sidebar` - Menu điều hướng chính
- `Footer` - Footer

### Common Components
- `Button` - Buttons với variants khác nhau
- `Input` - Form inputs
- `Select` - Dropdown selects
- `Modal` - Modal dialogs
- `Card` - Content cards
- `Table` - Data tables
- `Toast` - Notifications

### KPI Components
- `KPICard` - Hiển thị KPI summary
- `KPIForm` - Form tạo/sửa KPI
- `KPIList` - Danh sách KPIs
- `KPIDetail` - Chi tiết KPI
- `FileUpload` - Upload files
- `CommentSection` - Bình luận

---

## 🔌 API Integration

### Authentication

```javascript
import { login, logout, refreshToken } from './services/auth';

// Login
const { access_token, user } = await login(email, password);

// Refresh token
const { access_token } = await refreshToken(refresh_token);

// Logout
await logout();
```

### KPI Operations

```javascript
import { getKPIs, createKPI, updateKPI } from './services/kpi';

// Get KPIs with filters
const { items, total } = await getKPIs({
  year: 2024,
  quarter: 'Q1',
  status: 'approved'
});

// Create KPI
const kpi = await createKPI({
  title: 'Improve uptime',
  year: 2024,
  quarter: 'Q1',
  target_value: '99.9'
});

// Update KPI
await updateKPI(kpiId, { current_value: '99.8' });
```

---

## 🎨 Styling

### Tailwind CSS

Project sử dụng Tailwind CSS cho styling:

```jsx
<button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click Me
</button>
```

### Custom Theme

Customize theme trong `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
      }
    }
  }
}
```

---

## 🧭 Routing

### Protected Routes

```jsx
import { Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
```

### Role-Based Routes

```jsx
function AdminRoute({ children }) {
  const { user } = useAuth();

  if (user.role !== 'admin') {
    return <Navigate to="/" replace />;
  }

  return children;
}
```

---

## 🧪 Testing

```bash
# Run tests (nếu đã config)
npm test

# Run E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

---

## 🐳 Docker

### Development

```bash
# Build image
docker build -t kpi-frontend .

# Run container
docker run -d \
  --name kpi-frontend \
  -p 80:80 \
  kpi-frontend
```

### Production

Xem `deployment/docker-compose.prod.yml` để biết production setup.

---

## 🔧 Development

### Code Style

```bash
# Format code
npm run format

# Lint
npm run lint

# Fix lint errors
npm run lint:fix
```

### Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=KPI Management System
```

Truy cập trong code:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

---

## 📱 Responsive Design

Project được thiết kế responsive cho:
- Desktop (≥1024px)
- Tablet (768px - 1023px)
- Mobile (≤767px)

### Breakpoints (Tailwind)

```jsx
<div className="
  w-full
  md:w-1/2
  lg:w-1/3
">
  Responsive width
</div>
```

---

## ♿ Accessibility

### Best Practices

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus indicators
- Alt text cho images
- Color contrast (WCAG AA)

### Example

```jsx
<button
  aria-label="Close dialog"
  onClick={onClose}
>
  <CloseIcon />
</button>
```

---

## 📚 Tài Liệu Liên Quan

- [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) - Kiến trúc hệ thống
- [../docs/API.md](../docs/API.md) - Tài liệu API
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 🤝 Contributing

Xem [../CONTRIBUTING.md](../CONTRIBUTING.md) để biết hướng dẫn đóng góp.

---

## 📦 Scripts

```json
{
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "lint": "eslint . --ext js,jsx",
  "lint:fix": "eslint . --ext js,jsx --fix",
  "format": "prettier --write \"src/**/*.{js,jsx,css}\"",
  "test": "vitest",
  "test:e2e": "playwright test"
}
```

---

## 🎯 Performance Tips

1. **Code Splitting**: Sử dụng `React.lazy()` và `Suspense`
2. **Memoization**: Dùng `React.memo`, `useMemo`, `useCallback`
3. **Virtual Scrolling**: Cho long lists
4. **Image Optimization**: Lazy load images
5. **Bundle Analysis**: `npm run build -- --analyze`

---

## 🚀 Deployment

### Build for Production

```bash
# Build optimized bundle
npm run build

# Preview production build
npm run preview
```

### Deploy với Docker

```bash
# Build Docker image
docker build -t kpi-frontend:latest .

# Run production container
docker run -d -p 80:80 kpi-frontend:latest
```

---

**Happy Coding!** 🎉
