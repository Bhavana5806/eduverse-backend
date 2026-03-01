# EduVerse AI - Frontend Integration Guide

## 🎯 Overview

This guide provides comprehensive instructions for integrating the EduVerse AI backend with frontend applications. The system supports React, Vue.js, Angular, and vanilla JavaScript implementations.

## 🏗️ Frontend Architecture

### Recommended Tech Stack

#### Option 1: React + TypeScript (Recommended)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0",
    "zustand": "^4.3.0",
    "react-hook-form": "^7.43.0",
    "react-query": "^3.39.0",
    "@mui/material": "^5.11.0",
    "@mui/icons-material": "^5.11.0",
    "chart.js": "^4.2.0",
    "react-chartjs-2": "^5.2.0"
  }
}
```

#### Option 2: Vue.js + TypeScript
```json
{
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.1.0",
    "axios": "^1.3.0",
    "pinia": "^2.1.0",
    "vee-validate": "^4.6.0",
    "chart.js": "^4.2.0",
    "@vue/chartjs": "^5.2.0",
    "@mui/material": "^5.11.0"
  }
}
```

#### Option 3: Angular
```json
{
  "dependencies": {
    "@angular/core": "^15.0.0",
    "@angular/common": "^15.0.0",
    "@angular/router": "^15.0.0",
    "@angular/forms": "^15.0.0",
    "rxjs": "^7.8.0",
    "chart.js": "^4.2.0",
    "ng2-charts": "^4.0.0",
    "@angular/material": "^15.0.0"
  }
}
```

## 🔌 API Integration

### Authentication Service

#### React Implementation
```typescript
// services/authService.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.eduverse.ai/api/v1';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  role: 'student' | 'teacher' | 'admin' | 'mentor';
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    access_token: string;
    refresh_token: string;
    user: any;
  };
}

class AuthService {
  private token: string | null = null;
  private refreshToken: string | null = null;

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
      this.setTokens(response.data.data.access_token, response.data.data.refresh_token);
      return response.data;
    } catch (error) {
      throw new Error('Login failed');
    }
  }

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
      return response.data;
    } catch (error) {
      throw new Error('Registration failed');
    }
  }

  async refreshToken(): Promise<string> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
        refresh_token: this.refreshToken
      });
      
      this.setTokens(response.data.data.access_token, response.data.data.refresh_token);
      return response.data.data.access_token;
    } catch (error) {
      this.logout();
      throw new Error('Token refresh failed');
    }
  }

  setTokens(accessToken: string, refreshToken: string) {
    this.token = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('accessToken');
    }
    return this.token;
  }

  logout() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  getAuthHeaders() {
    const token = this.getToken();
    return {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
  }
}

export const authService = new AuthService();
```

#### Vue.js Implementation
```typescript
// services/authService.ts
import axios from 'axios';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'https://api.eduverse.ai/api/v1';

export class AuthService {
  private token: string | null = null;
  private refreshToken: string | null = null;

  async login(credentials: any) {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    this.setTokens(response.data.data.access_token, response.data.data.refresh_token);
    return response.data;
  }

  async register(userData: any) {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
  }

  setTokens(accessToken: string, refreshToken: string) {
    this.token = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('accessToken');
    }
    return this.token;
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  logout() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  getAuthHeaders() {
    const token = this.getToken();
    return {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
  }
}

export const authService = new AuthService();
```

### API Service Layer

#### React Implementation
```typescript
// services/apiService.ts
import axios, { AxiosResponse } from 'axios';
import { authService } from './authService';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.eduverse.ai/api/v1';

class ApiService {
  private axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
  });

  constructor() {
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth headers
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = authService.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token refresh
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          try {
            const newToken = await authService.refreshToken();
            error.config.headers.Authorization = `Bearer ${newToken}`;
            return this.axiosInstance.request(error.config);
          } catch (refreshError) {
            authService.logout();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.axiosInstance.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.axiosInstance.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.axiosInstance.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.axiosInstance.delete(url);
    return response.data;
  }
}

export const apiService = new ApiService();
```

## 🎨 UI Components

### Video Player Component with Anti-Distraction

#### React Implementation
```typescript
// components/VideoPlayer.tsx
import React, { useEffect, useRef, useState } from 'react';
import { Box, Typography, LinearProgress, Alert } from '@mui/material';
import { authService } from '../services/authService';

interface VideoPlayerProps {
  videoUrl: string;
  thumbnailUrl?: string;
  title: string;
  duration: number;
  sessionId: string;
  sessionKey: string;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({
  videoUrl,
  thumbnailUrl,
  title,
  duration,
  sessionId,
  sessionKey
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [focusScore, setFocusScore] = useState(1.0);
  const [distractionsCount, setDistractionsCount] = useState(0);
  const [isLocked, setIsLocked] = useState(false);
  const [lockUntil, setLockUntil] = useState<Date | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const activityInterval = useRef<NodeJS.Timeout | null>(null);

  // Anti-distraction monitoring
  useEffect(() => {
    const monitorActivity = async () => {
      const activityData = {
        tab_switch_detected: document.hidden,
        window_focus_lost: !document.hasFocus(),
        ai_tool_detected: false, // This would need additional detection logic
        multitasking_indicators: distractionsCount,
        last_activity: new Date().toISOString(),
        distractions: []
      };

      try {
        const response = await fetch('/api/v1/anti-distraction/validate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionKey}`
          },
          body: JSON.stringify({
            session_id: sessionId,
            session_key: sessionKey,
            activity_data: activityData
          })
        });

        const result = await response.json();

        if (result.success) {
          setFocusScore(result.session_state.focus_score);
          setDistractionsCount(result.session_state.distractions_count);
          
          if (result.session_state.state === 'locked') {
            setIsLocked(true);
            setLockUntil(new Date(result.locked_until));
          }
        }
      } catch (error) {
        console.error('Activity validation failed:', error);
      }
    };

    // Start monitoring
    activityInterval.current = setInterval(monitorActivity, 30000); // Every 30 seconds

    // Event listeners for distraction detection
    const handleVisibilityChange = () => {
      if (document.hidden) {
        setDistractionsCount(prev => prev + 1);
      }
    };

    const handleWindowBlur = () => {
      setDistractionsCount(prev => prev + 1);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('blur', handleWindowBlur);

    return () => {
      if (activityInterval.current) {
        clearInterval(activityInterval.current);
      }
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('blur', handleWindowBlur);
    };
  }, [sessionId, sessionKey, distractionsCount]);

  // Lock screen component
  if (isLocked && lockUntil && new Date() < lockUntil) {
    return (
      <Box sx={{ 
        position: 'fixed', 
        top: 0, 
        left: 0, 
        width: '100%', 
        height: '100%', 
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        color: 'white',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 9999
      }}>
        <Box sx={{ 
          textAlign: 'center', 
          backgroundColor: '#333', 
          padding: 4, 
          borderRadius: 2,
          boxShadow: '0 0 20px rgba(0,0,0,0.5)'
        }}>
          <Typography variant="h4" color="error" gutterBottom>
            Session Locked
          </Typography>
          <Typography variant="body1" gutterBottom>
            Due to excessive distractions, your session has been locked.
          </Typography>
          <Typography variant="h6" gutterBottom>
            Session will be available again at: {lockUntil.toLocaleString()}
          </Typography>
          <button 
            onClick={() => window.location.reload()}
            style={{
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '16px',
              marginTop: '20px'
            }}
          >
            Try Again
          </button>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: '800px', margin: '0 auto', padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        {title}
      </Typography>
      
      {/* Focus Indicator */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="body2" color={focusScore > 0.7 ? 'success.main' : 'warning.main'}>
          Focus: {(focusScore * 100).toFixed(0)}%
        </Typography>
        <Typography variant="body2" color="error">
          Distractions: {distractionsCount}
        </Typography>
      </Box>

      {/* Progress Bar */}
      <LinearProgress 
        variant="determinate" 
        value={(currentTime / duration) * 100} 
        sx={{ mb: 2 }}
      />

      {/* Video Element */}
      <video 
        ref={videoRef}
        src={videoUrl}
        controls
        style={{ width: '100%', height: 'auto', borderRadius: 8 }}
        onTimeUpdate={(e) => setCurrentTime((e.target as HTMLVideoElement).currentTime)}
      >
        Your browser does not support the video tag.
      </video>

      {/* Distraction Alerts */}
      {distractionsCount > 0 && (
        <Alert severity="warning" sx={{ mt: 2 }}>
          You have been distracted {distractionsCount} time(s). Please focus on your learning.
        </Alert>
      )}

      {/* Focus Tips */}
      {focusScore < 0.5 && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Low focus detected. Consider taking a short break and returning with fresh focus.
        </Alert>
      )}
    </Box>
  );
};

export default VideoPlayer;
```

### Assessment Component

#### React Implementation
```typescript
// components/AssessmentForm.tsx
import React, { useState } from 'react';
import { Box, Typography, Button, RadioGroup, FormControlLabel, Radio, Alert } from '@mui/material';
import { apiService } from '../services/apiService';

interface AssessmentQuestion {
  id: string;
  question: string;
  options: string[];
  correctAnswer: string;
}

interface AssessmentFormProps {
  subject: string;
  topic: string;
  studentId: number;
}

const AssessmentForm: React.FC<AssessmentFormProps> = ({ subject, topic, studentId }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [isCompleted, setIsCompleted] = useState(false);
  const [result, setResult] = useState<any>(null);

  const questions: AssessmentQuestion[] = [
    {
      id: 'q1',
      question: 'What is the capital of France?',
      options: ['London', 'Paris', 'Berlin', 'Madrid'],
      correctAnswer: 'Paris'
    },
    {
      id: 'q2',
      question: 'What is 2 + 2?',
      options: ['3', '4', '5', '6'],
      correctAnswer: '4'
    }
  ];

  const handleAnswer = (questionId: string, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleSubmit = async () => {
    const score = questions.reduce((acc, q) => {
      return acc + (answers[q.id] === q.correctAnswer ? 1 : 0);
    }, 0);

    const maxScore = questions.length;
    const percentage = (score / maxScore) * 100;

    try {
      const response = await apiService.post('/students/{studentId}/assessments', {
        subject,
        topic,
        score,
        max_score: maxScore,
        percentage,
        time_taken: 300, // 5 minutes
        difficulty: 'beginner',
        complexity_level: 5,
        question_count: questions.length,
        assessment_type: 'diagnostic'
      });

      setResult(response.data);
      setIsCompleted(true);
    } catch (error) {
      console.error('Assessment submission failed:', error);
    }
  };

  if (isCompleted && result) {
    return (
      <Box sx={{ maxWidth: '600px', margin: '0 auto', padding: 3 }}>
        <Typography variant="h4" gutterBottom>
          Assessment Results
        </Typography>
        
        <Alert severity="success" sx={{ mb: 3 }}>
          Score: {result.data.analysis.percentage}%
        </Alert>

        <Typography variant="h6" gutterBottom>
          Analysis:
        </Typography>
        <Typography>{result.data.analysis.status}</Typography>

        {result.data.recommendation && (
          <Alert severity="info" sx={{ mt: 3 }}>
            {result.data.recommendation}
          </Alert>
        )}
      </Box>
    );
  }

  return (
    <Box sx={{ maxWidth: '800px', margin: '0 auto', padding: 3 }}>
      <Typography variant="h4" gutterBottom>
        {topic} Assessment
      </Typography>
      
      <Typography variant="body1" color="text.secondary" gutterBottom>
        Question {currentQuestion + 1} of {questions.length}
      </Typography>

      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          {questions[currentQuestion].question}
        </Typography>
        
        <RadioGroup
          value={answers[questions[currentQuestion].id] || ''}
          onChange={(e) => handleAnswer(questions[currentQuestion].id, e.target.value)}
        >
          {questions[currentQuestion].options.map((option, index) => (
            <FormControlLabel
              key={index}
              value={option}
              control={<Radio />}
              label={option}
            />
          ))}
        </RadioGroup>
      </Box>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button
          variant="outlined"
          disabled={currentQuestion === 0}
          onClick={() => setCurrentQuestion(prev => prev - 1)}
        >
          Previous
        </Button>
        
        {currentQuestion < questions.length - 1 ? (
          <Button
            variant="contained"
            disabled={!answers[questions[currentQuestion].id]}
            onClick={() => setCurrentQuestion(prev => prev + 1)}
          >
            Next
          </Button>
        ) : (
          <Button
            variant="contained"
            color="primary"
            disabled={Object.keys(answers).length !== questions.length}
            onClick={handleSubmit}
          >
            Submit Assessment
          </Button>
        )}
      </Box>
    </Box>
  );
};

export default AssessmentForm;
```

### Dashboard Component

#### React Implementation
```typescript
// components/StudentDashboard.tsx
import React, { useEffect, useState } from 'react';
import { Box, Typography, Grid, Card, CardContent, LinearProgress } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { apiService } from '../services/apiService';

interface DashboardData {
  student_info: any;
  current_assessment: any;
  weakness_analysis: any;
  learning_path: any;
  simulation_progress: any[];
  career_profile: any;
  progress_analytics: any;
}

const StudentDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await apiService.get('/dashboard/1'); // Replace with actual student ID
        setDashboardData(response.data.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography>Loading dashboard...</Typography>
      </Box>
    );
  }

  if (!dashboardData) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <Typography>Failed to load dashboard data.</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h4" gutterBottom>
        Student Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Performance Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Overview
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Current Assessment: {dashboardData.current_assessment?.topic}
              </Typography>
              <Typography variant="h4" color="primary">
                {dashboardData.current_assessment?.percentage}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={dashboardData.current_assessment?.percentage || 0} 
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Weakness Analysis */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Weakness Analysis
              </Typography>
              {dashboardData.weakness_analysis?.weak_topics && (
                <Box>
                  {Object.entries(dashboardData.weakness_analysis.weak_topics).map(([topic, data]: [string, any]) => (
                    <Box key={topic} sx={{ mb: 2 }}>
                      <Typography variant="body2">{topic}</Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={data.score || 0} 
                        color="error"
                      />
                    </Box>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Learning Path */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Learning Path
              </Typography>
              {dashboardData.learning_path?.milestones && (
                <Grid container spacing={2}>
                  {Object.entries(dashboardData.learning_path.milestones).map(([id, milestone]: [string, any]) => (
                    <Grid item xs={12} sm={6} md={4} key={id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="body2">{milestone.name}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            Status: {milestone.status}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Simulation Progress */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Simulation Progress
              </Typography>
              {dashboardData.simulation_progress.map((sim, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Typography variant="body2">{sim.simulation?.name}</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={sim.mastery_score || 0} 
                    sx={{ mt: 1 }}
                  />
                  <Typography variant="caption" color="text.secondary">
                    Mastery: {(sim.mastery_score || 0).toFixed(0)}%
                  </Typography>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Progress Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Progress Analytics
              </Typography>
              {/* Chart implementation would go here */}
              <Box sx={{ height: 300 }}>
                {/* Chart.js or other chart library integration */}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentDashboard;
```

## 🎮 Simulation Integration

### WebGL/Canvas Simulation Component

#### React Implementation
```typescript
// components/SimulationCanvas.tsx
import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

interface SimulationCanvasProps {
  simulationType: string;
  difficulty: string;
  onComplete: (performance: number) => void;
}

const SimulationCanvas: React.FC<SimulationCanvasProps> = ({ simulationType, difficulty, onComplete }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    // Initialize Three.js scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x202025);
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(75, mountRef.current.clientWidth / mountRef.current.clientHeight, 0.1, 1000);
    camera.position.z = 5;
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
    mountRef.current.appendChild(renderer.domElement);

    rendererRef.current = renderer;

    // Add simulation objects based on type
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;

      renderer.render(scene, camera);
    };

    animate();

    // Cleanup
    return () => {
      if (rendererRef.current) {
        rendererRef.current.dispose();
      }
    };
  }, [simulationType, difficulty]);

  return (
    <div ref={mountRef} style={{ width: '100%', height: '400px' }}>
      {/* Three.js canvas will be rendered here */}
    </div>
  );
};

export default SimulationCanvas;
```

## 📱 Mobile App Integration

### React Native Implementation

#### Authentication Service for React Native
```typescript
// services/authService.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_BASE_URL = 'https://api.eduverse.ai/api/v1';

export class AuthService {
  async login(credentials: { email: string; password: string }) {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    await AsyncStorage.setItem('accessToken', response.data.data.access_token);
    await AsyncStorage.setItem('refreshToken', response.data.data.refresh_token);
    return response.data;
  }

  async getToken(): Promise<string | null> {
    return await AsyncStorage.getItem('accessToken');
  }

  async isAuthenticated(): Promise<boolean> {
    const token = await this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  async logout() {
    await AsyncStorage.removeItem('accessToken');
    await AsyncStorage.removeItem('refreshToken');
  }
}
```

#### Video Player for React Native
```typescript
// components/VideoPlayer.tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import Video from 'react-native-video';
import { authService } from '../services/authService';

interface VideoPlayerProps {
  videoUrl: string;
  title: string;
  duration: number;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoUrl, title, duration }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      
      <Video
        source={{ uri: videoUrl }}
        style={styles.video}
        controls={true}
        resizeMode="contain"
      />
      
      <Text style={styles.duration}>
        Duration: {Math.floor(duration / 60)}:{(duration % 60).toString().padStart(2, '0')}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  video: {
    width: '100%',
    height: 200,
    backgroundColor: '#000',
    marginBottom: 20,
  },
  duration: {
    fontSize: 16,
    color: '#666',
  },
});

export default VideoPlayer;
```

## 🔧 Configuration and Setup

### Environment Variables

#### React/Vue.js
```env
REACT_APP_API_URL=https://api.eduverse.ai/api/v1
REACT_APP_GOOGLE_API_KEY=your-google-api-key
REACT_APP_ENABLE_DEBUG=true
```

#### Angular
```env
API_URL=https://api.eduverse.ai/api/v1
GOOGLE_API_KEY=your-google-api-key
ENABLE_DEBUG=true
```

### Build Configuration

#### Webpack Configuration
```javascript
// webpack.config.js
module.exports = {
  // ... other config
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx']
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  devServer: {
    proxy: {
      '/api': {
        target: 'https://api.eduverse.ai',
        changeOrigin: true,
      }
    }
  }
};
```

#### Vite Configuration
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://api.eduverse.ai',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    minify: 'terser',
    sourcemap: true
  }
});
```

## 🚀 Deployment

### Static Site Deployment

#### Netlify
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

#### Vercel
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Mobile App Deployment

#### iOS (React Native)
```bash
# Build for iOS
npx react-native run-ios --configuration Release

# Archive for App Store
xcodebuild -workspace EduVerse.xcworkspace -scheme EduVerse -configuration Release -archivePath EduVerse.xcarchive archive
```

#### Android (React Native)
```bash
# Generate signed APK
cd android
./gradlew assembleRelease

# Generate signed AAB
./gradlew bundleRelease
```

## 🧪 Testing

### Jest + React Testing Library

```typescript
// __tests__/authService.test.ts
import { authService } from '../services/authService';

describe('AuthService', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('should login successfully', async () => {
    const mockResponse = {
      success: true,
      data: {
        access_token: 'mock-token',
        refresh_token: 'mock-refresh-token',
        user: { id: 1, email: 'test@example.com' }
      }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockResponse),
      })
    ) as jest.Mock;

    const result = await authService.login({
      email: 'test@example.com',
      password: 'password123'
    });

    expect(result).toEqual(mockResponse);
    expect(localStorage.getItem('accessToken')).toBe('mock-token');
  });

  test('should check authentication', () => {
    localStorage.setItem('accessToken', 'valid-token');
    expect(authService.isAuthenticated()).toBe(true);
  });
});
```

### Cypress E2E Testing

```javascript
// cypress/e2e/auth.cy.js
describe('Authentication', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('[data-cy=email-input]').type('test@example.com');
    cy.get('[data-cy=password-input]').type('password123');
    cy.get('[data-cy=login-button]').click();
    cy.url().should('include', '/dashboard');
  });

  it('should show error for invalid credentials', () => {
    cy.visit('/login');
    cy.get('[data-cy=email-input]').type('invalid@example.com');
    cy.get('[data-cy=password-input]').type('wrongpassword');
    cy.get('[data-cy=login-button]').click();
    cy.get('[data-cy=error-message]').should('be.visible');
  });
});
```

## 📊 Monitoring and Analytics

### Performance Monitoring

```typescript
// utils/performanceMonitor.ts
export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: any[] = [];

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  trackAPICall(endpoint: string, duration: number, success: boolean) {
    this.metrics.push({
      type: 'api_call',
      endpoint,
      duration,
      success,
      timestamp: Date.now()
    });
  }

  trackUserAction(action: string, duration?: number) {
    this.metrics.push({
      type: 'user_action',
      action,
      duration,
      timestamp: Date.now()
    });
  }

  getMetrics() {
    return this.metrics;
  }

  clearMetrics() {
    this.metrics = [];
  }
}

// Usage in API service
const performanceMonitor = PerformanceMonitor.getInstance();
performanceMonitor.trackAPICall('/api/v1/students/1/assessments', 250, true);
```

### Error Tracking

```typescript
// utils/errorTracker.ts
export class ErrorTracker {
  static reportError(error: Error, context?: any) {
    console.error('Error occurred:', error, context);
    
    // Send to error tracking service (e.g., Sentry)
    if (typeof window !== 'undefined' && (window as any).Sentry) {
      (window as any).Sentry.captureException(error, {
        extra: context
      });
    }
  }
}

// Usage
try {
  await apiService.get('/some-endpoint');
} catch (error) {
  ErrorTracker.reportError(error as Error, { endpoint: '/some-endpoint' });
}
```

## 🎨 Design System

### Theme Configuration

```typescript
// theme/index.ts
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#007bff',
      light: '#64b5f6',
      dark: '#1976d2',
    },
    secondary: {
      main: '#6c757d',
      light: '#9e9e9e',
      dark: '#424242',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});

export default theme;
```

### Component Library

```typescript
// components/ui/index.ts
export { default as Button } from './Button';
export { default as Card } from './Card';
export { default as Input } from './Input';
export { default as Modal } from './Modal';
export { default as LoadingSpinner } from './LoadingSpinner';
export { default as ErrorBoundary } from './ErrorBoundary';
```

## 📱 Accessibility

### ARIA Labels and Keyboard Navigation

```typescript
// components/AccessibleVideoPlayer.tsx
import React from 'react';
import { Box, Typography, IconButton } from '@mui/material';
import { PlayArrow, Pause, VolumeUp, Fullscreen } from '@mui/icons-material';

const AccessibleVideoPlayer: React.FC = () => {
  return (
    <Box
      role="application"
      aria-label="Video player"
      sx={{
        position: 'relative',
        width: '100%',
        aspectRatio: '16 / 9',
        backgroundColor: '#000',
      }}
    >
      <video
        aria-label="Educational video content"
        aria-describedby="video-description"
        controls
      />
      
      <Box
        id="video-description"
        sx={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.7)',
          color: 'white',
          padding: 2,
        }}
      >
        <Typography variant="body2">
          Press Space to play/pause, M to mute/unmute, F for fullscreen
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
          <IconButton
            aria-label="Play/Pause"
            aria-pressed="false"
            size="small"
          >
            <PlayArrow />
          </IconButton>
          
          <IconButton
            aria-label="Mute/Unmute"
            aria-pressed="false"
            size="small"
          >
            <VolumeUp />
          </IconButton>
          
          <IconButton
            aria-label="Fullscreen"
            size="small"
          >
            <Fullscreen />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};
```

## 🎯 Performance Optimization

### Code Splitting

```typescript
// App.tsx
import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Assessment = React.lazy(() => import('./pages/Assessment'));
const VideoPlayer = React.lazy(() => import('./pages/VideoPlayer'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/assessment" element={<Assessment />} />
        <Route path="/video/:id" element={<VideoPlayer />} />
      </Routes>
    </Suspense>
  );
}
```

### Image Optimization

```typescript
// components/OptimizedImage.tsx
import React, { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  placeholder?: string;
}

const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width,
  height,
  placeholder
}) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div style={{ position: 'relative', width, height }}>
      {placeholder && (
        <img
          src={placeholder}
          alt=""
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            filter: 'blur(5px)',
            transition: 'opacity 0.3s'
          }}
        />
      )}
      
      <img
        src={src}
        alt={alt}
        onLoad={() => setIsLoaded(true)}
        style={{
          width: '100%',
          height: '100%',
          opacity: isLoaded ? 1 : 0,
          transition: 'opacity 0.3s',
        }}
      />
    </div>
  );
};
```

## 🚀 Next Steps

1. **Implement State Management**: Set up Redux, Zustand, or Pinia for state management
2. **Add Form Validation**: Implement comprehensive form validation with libraries like Yup or Zod
3. **Set Up CI/CD**: Configure continuous integration and deployment pipelines
4. **Performance Monitoring**: Implement real-user monitoring and performance tracking
5. **Accessibility Testing**: Conduct thorough accessibility audits and testing
6. **Mobile Optimization**: Ensure responsive design and mobile-first approach
7. **SEO Optimization**: Implement proper meta tags, structured data, and SSR/SSG
8. **Security Hardening**: Implement Content Security Policy, input sanitization, and security headers

## 📞 Support

For additional support and questions:
- **Documentation**: [API Documentation](API_DOCUMENTATION.md)
- **GitHub Issues**: Report bugs and feature requests
- **Community Forum**: Join our developer community
- **Email Support**: support@eduverse.ai

---

**Last Updated**: March 2024