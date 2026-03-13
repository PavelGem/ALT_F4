// frontend/src/pages/MainPage.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Добавляем для редиректа
import { useUsers } from '../hooks/useUsers';
import { useAuth } from '../contexts/AuthContext'; // Добавляем для logout
import api from '../utils/api';
import UserList from '../components/UserList';  
import UserSearch from '../components/UserSearch';
import styles from './MainPage.module.css';

function MainPage() {
    const navigate = useNavigate();
    const { logout, user } = useAuth(); // Получаем функцию logout и данные пользователя
    const [message, setMessage] = useState('Проверка связи...');
    const { users, loading, error, searchUser } = useUsers();

    // Проверка связи с бэкендом
    useEffect(() => {
        const checkBackend = async () => {
            try {
                const response = await api.get('/');
                setMessage(response.data?.message || '✅ Связь с бэкендом есть');
            } catch (err) {
                setMessage('❌ Ошибка связи: ' + (err.message || 'неизвестная ошибка'));
                console.error('Backend connection error:', err);
            }
        };

        checkBackend();
    }, []);

    // Обработчик выхода
    const handleLogout = () => {
        logout(); // Очищаем токены и данные пользователя
        navigate('/auth/login'); // Перенаправляем на страницу входа
    };

    return (
        <div className={styles.container}>
            {/* Шапка с приветствием и кнопкой выхода */}
            <div className={styles.header}>
                <h1 className={styles.title}>📊 Клуб ALT+F4</h1>
                <div className={styles.userInfo}>
                    {user && (
                        <span className={styles.welcomeText}>
                            👋 Привет, {user.full_name || user.email}!
                        </span>
                    )}
                    <button 
                        onClick={handleLogout}
                        className={styles.logoutButton}
                    >
                        Выйти
                    </button>
                </div>
            </div>
            
            {/* Статус бэкенда */}
            <div className={styles.statusCard}>
                <strong>Статус бэкенда:</strong> {message}
            </div>

            {/* Ошибки */}
            {error && (
                <div className={styles.errorCard}>
                    <strong>❌ Ошибка:</strong> {error}
                </div>
            )}

            {/* Список пользователей */}
            <section className={styles.section}>
                <h2 className={styles.sectionTitle}>👥 Все пользователи</h2>
                <UserList users={users} loading={loading} />
            </section>

            {/* Поиск */}
            <section className={styles.section}>
                <UserSearch onSearch={searchUser} loading={loading} />
            </section>

            {/* Информация */}
            <div className={styles.infoCard}>
                <h3>Информация:</h3>
                <ul>
                    <li>Бэкенд: <a href="http://localhost:8000" target="_blank" rel="noreferrer">http://localhost:8000</a></li>
                    <li>Документация: <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">http://localhost:8000/docs</a></li>
                </ul>
            </div>
        </div>
    );
}

export default MainPage;