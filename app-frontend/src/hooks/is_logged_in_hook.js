import { useEffect, useState } from 'react';
import { checkUserLoggedIn } from '../handlers/auth_handler';

export const IsLoggedInHook = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const checkLoginStatus = async () => {
      const [logged_in_result, user_id_result] = await checkUserLoggedIn();
      setIsLoggedIn(logged_in_result);
      setUserId(user_id_result);
    };

    checkLoginStatus().then();
  }, []);

  return [isLoggedIn, userId];
};
