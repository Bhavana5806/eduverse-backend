import React, { useEffect } from 'react';
import { Box, Typography, Grid, Card, CardContent, LinearProgress } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { apiService } from '../services/api';

interface DashboardData {
  student_info: any;
  current_assessment: any;
  weakness_analysis: any;
  learning_path: any;
  simulation_progress: any[];
  career_profile: any;
  progress_analytics: any;
}

const DashboardPage: React.FC = () => {
  const { data: dashboardData, isLoading, error } = useQuery<DashboardData>({
    queryKey: ['dashboard'],
    queryFn: () => apiService.get('/dashboard/1'), // Replace with actual student ID
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <Typography>Loading dashboard...</Typography>
      </Box>
    );
  }

  if (error || !dashboardData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
        <Typography color="error">Failed to load dashboard data.</Typography>
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
              <Box sx={{ height: 300 }}>
                {/* Chart.js or other chart library integration would go here */}
                <Typography variant="body2" color="text.secondary">
                  Progress visualization coming soon...
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;