import { useState, useEffect } from 'react';
import api from '../utils/api';

export const useUsers = () => {
  const [users, setUsers] = useState([]); // Всегда массив
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Загрузка всех пользователей
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await api.get('/users');
      
      // Убедимся, что users - это массив
      let usersData = response.data;
      
      // Проверяем структуру ответа
      if (usersData && typeof usersData === 'object') {
        // Если ответ в формате { users: [...], count: ... }
        if (usersData.users && Array.isArray(usersData.users)) {
          usersData = usersData.users;
        }
        // Если ответ просто объект, но не массив
        else if (!Array.isArray(usersData)) {
          console.warn('Users data is not an array:', usersData);
          usersData = []; // Превращаем в пустой массив
        }
      } else if (!Array.isArray(usersData)) {
        usersData = [];
      }
      
      setUsers(usersData);
      setError(null);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError(err.response?.data?.detail || err.message || 'Ошибка загрузки пользователей');
      setUsers([]); // При ошибке - пустой массив
    } finally {
      setLoading(false);
    }
  };

  // Поиск пользователя по имени/email
  const searchUser = async (query) => {
    if (!query.trim()) {
      fetchUsers();
      return;
    }

    try {
      setLoading(true);
      const response = await api.get(`/users/search?q=${encodeURIComponent(query)}`);
      
      let usersData = response.data;
      
      // Проверяем структуру ответа
      if (usersData && typeof usersData === 'object') {
        if (usersData.users && Array.isArray(usersData.users)) {
          usersData = usersData.users;
        } else if (!Array.isArray(usersData)) {
          usersData = [];
        }
      } else if (!Array.isArray(usersData)) {
        usersData = [];
      }
      
      setUsers(usersData);
      setError(null);
    } catch (err) {
      console.error('Error searching users:', err);
      
      // Если нет эндпоинта поиска, фильтруем локально
      try {
        const response = await api.get('/users');
        let allUsers = response.data;
        
        if (allUsers && typeof allUsers === 'object') {
          if (allUsers.users && Array.isArray(allUsers.users)) {
            allUsers = allUsers.users;
          } else if (!Array.isArray(allUsers)) {
            allUsers = [];
          }
        }
        
        const filtered = allUsers.filter(user => 
          user.full_name?.toLowerCase().includes(query.toLowerCase()) ||
          user.email?.toLowerCase().includes(query.toLowerCase())
        );
        setUsers(filtered);
      } catch (filterErr) {
        setError('Ошибка поиска пользователей');
        setUsers([]);
      }
    } finally {
      setLoading(false);
    }
  };

  return { users, loading, error, searchUser };
};