import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
    const [message, setMessage] = React.useState('Загрузка...');
    const [users, setUsers] = React.useState([]);
    const [email, setEmail] = React.useState('');
    const [userInfo, setUserInfo] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);

    // Проверяем связь с бэкендом и загружаем пользователей
    React.useEffect(() => {
        // Проверка связи
        fetch('http://localhost:8000/')
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log('Ответ от /:', data);
                setMessage(data.message || 'Связь с бэкендом есть');
            })
            .catch(err => {
                console.error('Ошибка связи:', err);
                setMessage('❌ Ошибка связи: ' + err.message);
            });

        // Загружаем список пользователей
        fetch('http://localhost:8000/users')
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                console.log('Ответ от /users:', data);
                // Проверяем структуру ответа
                if (data && data.users) {
                    setUsers(data.users);
                } else if (Array.isArray(data)) {
                    // Если сервер вернул просто массив
                    setUsers(data);
                } else {
                    console.warn('Неожиданный формат данных:', data);
                    setUsers([]);
                }
            })
            .catch(err => {
                console.error('Ошибка загрузки пользователей:', err);
                setError('Не удалось загрузить пользователей: ' + err.message);
            });
    }, []);

    // Поиск пользователя по email
    const findUser = () => {
        if (!email) {
            alert('Введите email');
            return;
        }
        
        setLoading(true);
        setUserInfo(null);
        
        fetch(`http://localhost:8000/users/${encodeURIComponent(email)}`)
            .then(res => {
                if (!res.ok) {
                    if (res.status === 404) return null;
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                console.log('Ответ от /users/email:', data);
                if (data === null) {
                    setUserInfo({ notFound: true });
                } else if (data && data.user) {
                    setUserInfo(data.user);
                } else if (data && data.email) {
                    // Если сервер вернул самого пользователя
                    setUserInfo(data);
                } else {
                    setUserInfo(null);
                }
                setLoading(false);
            })
            .catch(err => {
                console.error('Ошибка поиска:', err);
                setError('Ошибка поиска: ' + err.message);
                setLoading(false);
            });
    };

    return (
        <div style={{ 
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            maxWidth: '800px',
            margin: '0 auto',
            padding: '20px',
            color: '#333'
        }}>
            <h1 style={{ marginBottom: '20px' }}>📊 Клуб ALT+F4</h1>
            
            {/* Статус бэкенда */}
            <div style={{
                backgroundColor: '#f8f9fa',
                padding: '15px',
                borderRadius: '8px',
                marginBottom: '25px',
                border: '1px solid #dee2e6'
            }}>
                <strong>Статус бэкенда:</strong> {message}
            </div>

            {/* Ошибки */}
            {error && (
                <div style={{
                    backgroundColor: '#f8d7da',
                    color: '#721c24',
                    padding: '15px',
                    borderRadius: '8px',
                    marginBottom: '25px',
                    border: '1px solid #f5c6cb'
                }}>
                    <strong>❌ Ошибка:</strong> {error}
                </div>
            )}

            {/* Список пользователей */}
            <div style={{ marginBottom: '30px' }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '15px' }}>👥 Все пользователи</h2>
                {users.length > 0 ? (
                    <ul style={{ 
                        listStyle: 'none', 
                        padding: 0,
                        margin: 0
                    }}>
                        {users.map(user => (
                            <li key={user.email} style={{
                                padding: '12px',
                                backgroundColor: '#fff',
                                border: '1px solid #dee2e6',
                                borderRadius: '6px',
                                marginBottom: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '10px'
                            }}>
                                <span style={{ fontSize: '1.2rem' }}>📧</span>
                                <div style={{ flex: 1 }}>
                                    <div><strong>{user.email}</strong></div>
                                    {user.full_name && <div style={{ fontSize: '0.9rem', color: '#666' }}>{user.full_name}</div>}
                                </div>
                                <span style={{
                                    padding: '4px 8px',
                                    borderRadius: '4px',
                                    fontSize: '0.85rem',
                                    backgroundColor: user.is_active ? '#d4edda' : '#f8d7da',
                                    color: user.is_active ? '#155724' : '#721c24'
                                }}>
                                    {user.is_active ? 'Активен' : 'Неактивен'}
                                </span>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p style={{ color: '#666', fontStyle: 'italic' }}>
                        {loading ? 'Загрузка...' : 'Нет пользователей'}
                    </p>
                )}
            </div>

            {/* Поиск пользователя по email */}
            <div style={{ marginBottom: '30px' }}>
                <h2 style={{ fontSize: '1.5rem', marginBottom: '15px' }}>🔍 Поиск пользователя</h2>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
                    <input
                        type="email"
                        placeholder="Введите email (например: user1@example.com)"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{
                            flex: 1,
                            padding: '10px',
                            borderRadius: '6px',
                            border: '1px solid #dee2e6',
                            fontSize: '1rem'
                        }}
                    />
                    <button
                        onClick={findUser}
                        disabled={loading}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#007bff',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            fontSize: '1rem',
                            cursor: 'pointer',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Поиск...' : 'Найти'}
                    </button>
                </div>

                {/* Результат поиска */}
                {userInfo && (
                    <div style={{
                        padding: '15px',
                        backgroundColor: '#e8f4fd',
                        borderRadius: '8px',
                        border: '1px solid #b8e0ff'
                    }}>
                        {userInfo.notFound ? (
                            <p style={{ color: '#721c24', margin: 0 }}>
                                ❌ Пользователь с таким email не найден
                            </p>
                        ) : (
                            <>
                                <h3 style={{ margin: '0 0 10px 0', fontSize: '1.1rem' }}>Результат:</h3>
                                <p style={{ margin: '5px 0' }}>
                                    <strong>Email:</strong> {userInfo.email}
                                </p>
                                {userInfo.full_name && (
                                    <p style={{ margin: '5px 0' }}>
                                        <strong>Имя:</strong> {userInfo.full_name}
                                    </p>
                                )}
                                <p style={{ margin: '5px 0' }}>
                                    <strong>Статус:</strong> 
                                    <span style={{
                                        marginLeft: '8px',
                                        padding: '2px 6px',
                                        borderRadius: '4px',
                                        fontSize: '0.85rem',
                                        backgroundColor: userInfo.is_active ? '#d4edda' : '#f8d7da',
                                        color: userInfo.is_active ? '#155724' : '#721c24'
                                    }}>
                                        {userInfo.is_active ? 'Активен' : 'Неактивен'}
                                    </span>
                                </p>
                            </>
                        )}
                    </div>
                )}
            </div>

            <div style={{ 
                backgroundColor: '#f0f0f0', 
                padding: '10px',
                borderRadius: '5px'
            }}>
                <h3>Информация:</h3>
                <ul>
                    <li>Бэкенд: <a href="http://localhost:8000">http://localhost:8000</a></li>
                    <li>Документация API: <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
                </ul>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);


/*
import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
    const [message, setMessage] = React.useState('Загрузка...');
    
    // Проверяем связь с бэкендом
    React.useEffect(() => {
        fetch('http://localhost:8000/')
            .then(res => res.json())
            .then(data => setMessage(data.message || 'Связь с бэкендом есть'))
            .catch(err => setMessage('Ошибка связи с бэкендом: ' + err.message));
    }, []);

    return (
        <div style={{ 
            fontFamily: 'Arial, sans-serif',
            maxWidth: '800px',
            margin: '0 auto',
            padding: '20px'
        }}>
            <h1 style={{ color: '#333' }}>Моё React приложение</h1>
            <p>Статус бэкенда: <strong>{message}</strong></p>
            
            <h2>Тестовые данные</h2>
            <p>Здесь будет ваше приложение...</p>
            
            <div style={{ 
                backgroundColor: '#f0f0f0', 
                padding: '10px',
                borderRadius: '5px'
            }}>
                <h3>Информация:</h3>
                <ul>
                    <li>Бэкенд: <a href="http://localhost:8000">http://localhost:8000</a></li>
                    <li>Документация API: <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></li>
                </ul>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
*/
