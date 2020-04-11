import express from 'express';
import { authController } from '../controllers';
import { checkToken as authMiddleware } from '../middleware';

export const authRoute = express.Router();

authRoute.post('/login', authController.login);
authRoute.get('/', authMiddleware, authController.index);
