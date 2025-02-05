import { useEffect, useState } from 'react';
import { checkUserLoggedIn } from '../handlers/auth_handler';

export const IsLoggedInHook = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLoginStatus = async () => {
      const loggedIn = await checkUserLoggedIn();
      setIsLoggedIn(loggedIn);
    };

    checkLoginStatus().then();
  }, []);

  return isLoggedIn;
};
