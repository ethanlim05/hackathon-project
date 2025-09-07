const baseUrl = 'http://localhost:5000/api'; // Backend API URL

/**
 * Verify plate format and check if it exists
 * Returns:
 *  - { status: 'new', plate, message }
 *  - { status: 'invalid', message }
 *  - { status: 'error', message }
 */
export async function verifyPlate(plate) {
  try {
    const response = await fetch(`${baseUrl}/verify-plate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plate: plate.toUpperCase().replace(/\s+/g, '') })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to verify plate');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error verifying plate:', error);
    return { status: 'error', message: error.message };
  }
}

/**
 * Validate car information
 * Returns:
 *  - { ok: true, message }
 *  - { ok: false, message, corrected?, errors? }
 */
export async function validateCar(car) {
  try {
    const response = await fetch(`${baseUrl}/validate-car`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(car)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to validate car');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error validating car:', error);
    return { ok: false, message: error.message };
  }
}

/**
 * Submit complete onboarding application
 * Returns:
 *  - { ok: true, applicationId, message }
 *  - { ok: false, message }
 */
export async function submitOnboarding(payload) {
  try {
    const response = await fetch(`${baseUrl}/submit-onboarding`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Submission failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error submitting onboarding:', error);
    return { ok: false, message: error.message };
  }
}

/**
 * Get available car brands
 */
export async function getBrands() {
  try {
    const response = await fetch(`${baseUrl}/brands`);
    if (!response.ok) throw new Error('Failed to fetch brands');
    const data = await response.json();
    return data.brands || [];
  } catch (error) {
    console.error('Error fetching brands:', error);
    return [];
  }
}

/**
 * Get models for a specific brand
 */
export async function getModels(brand) {
  try {
    const response = await fetch(`${baseUrl}/models/${encodeURIComponent(brand)}`);
    if (!response.ok) throw new Error('Failed to fetch models');
    const data = await response.json();
    return data.models || [];
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
  }
}

/**
 * Health check for backend
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${baseUrl}/health`);
    if (!response.ok) throw new Error('Backend not healthy');
    return await response.json();
  } catch (error) {
    console.error('Backend health check failed:', error);
    return { status: 'unhealthy' };
  }
}

