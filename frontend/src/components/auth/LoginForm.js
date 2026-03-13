// frontend/src/components/auth/LoginForm.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import styles from './LoginForm.module.css';  // Импортируем как styles

const LoginForm = () => {
  const navigate = useNavigate();
  const { login, error: authError } = useAuth();
  
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(formData.username, formData.password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Неверный email или пароль');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.box}>
        <h2 className={styles.title}>Добро пожаловать! 👋</h2>
        <p className={styles.subtitle}>Войдите в свой аккаунт</p>
        
        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label className={styles.label}>Email или имя пользователя</label>
            <input
              type="text"
              name="username"
              placeholder="example@mail.com"
              value={formData.username}
              onChange={handleChange}
              required
              className={styles.input}
            />
          </div>
          
          <div className={styles.formGroup}>
            <label className={styles.label}>Пароль</label>
            <input
              type="password"
              name="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              required
              className={styles.input}
            />
          </div>

          {(error || authError) && (
            <div className={styles.errorAlert}>
              {error || authError}
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className={`${styles.button} ${loading ? styles.buttonLoading : ''}`}
          >
            {loading ? 'Вход...' : 'Войти'}
          </button>

          <div className={styles.linkContainer}>
            <Link to="/auth/register" className={styles.link}>
              Нет аккаунта? Зарегистрироваться
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;