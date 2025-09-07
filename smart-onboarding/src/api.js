<<<<<<< Updated upstream
// Mock API for now - will be replaced with real backend later
const baseUrl = '/api'; // Will be replaced with backend URL

/**
 * Mock: Verify plate format and check if it exists
 * Returns:
 *  - { status: 'new', plate, message }
 *  - { status: 'invalid', message }
 *  - { status: 'error', message }
 */
export async function verifyPlate(plate) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  const plateUpper = plate.toUpperCase().replace(/\s+/g, '');
  
  // Basic plate format validation
  const platePattern = /^[A-Z]{1,3}[0-9]{1,4}[A-Z]?$/;
  
  if (!platePattern.test(plateUpper)) {
    return {
      status: 'invalid',
      message: 'Invalid plate format. Please use format like ABC 1234 or XYZ123'
    };
  }
  
  // For demo purposes, assume all valid plates are new
  return {
    status: 'new',
    plate: plateUpper,
    message: 'Plate format is valid'
  };
}

/**
 * Mock: Validate car information
=======
const baseUrl = 'http://localhost:5000/api'; // Backend API URL
import { VEHICLES } from './mockData';

/**
 * Mock-first: verify plate format and check if it exists in local VEHICLES.
 * Falls back to backend if you later wire it up.
 */
export async function verifyPlate(plate) {
  // simulate latency
  await new Promise(r => setTimeout(r, 300));
  const normalized = String(plate || '').toUpperCase().replace(/\s+/g, '');

  // basic plate pattern like ABC1234A or AB 1234
  const pattern = /^[A-Z]{1,3}[0-9]{1,4}[A-Z]?$/;
  if (!pattern.test(normalized)) {
    return { status: 'invalid', message: 'Invalid plate format. Use ABC1234 or ABC1234A' };
  }

  const hit = VEHICLES.find(v => v.plate === normalized);
  if (hit) return { status: 'existing', plate: hit.plate };
  return { status: 'new', plate: normalized, message: 'Plate format is valid' };
}

/**
 * Validate car information
>>>>>>> Stashed changes
 * Returns:
 *  - { ok: true, message }
 *  - { ok: false, message, corrected?, errors? }
 */
export async function validateCar(car) {
<<<<<<< Updated upstream
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300));
  
  const { brand, model, year } = car;
  
  // Basic validation
  if (!brand || !model || !year) {
    return {
      ok: false,
      message: 'All fields (brand, model, year) are required'
    };
  }
  
  // Mock some validation logic
  const currentYear = new Date().getFullYear();
  const yearNum = parseInt(year);
  
  if (yearNum < 1990 || yearNum > currentYear + 1) {
    return {
      ok: false,
      message: `Year must be between 1990 and ${currentYear + 1}`
    };
  }
  
  // For demo purposes, assume all valid inputs are correct
  return {
    ok: true,
    message: 'Vehicle information is valid'
  };
}

/**
 * Mock: Submit complete onboarding application
=======
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
>>>>>>> Stashed changes
 * Returns:
 *  - { ok: true, applicationId, message }
 *  - { ok: false, message }
 */
export async function submitOnboarding(payload) {
<<<<<<< Updated upstream
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800));
  
  // Generate a mock application ID
  const applicationId = `APP-${Math.floor(Math.random() * 100000).toString().padStart(5, '0')}`;
  
  console.log('Mock submission:', payload);
  
  return {
    ok: true,
    applicationId,
    message: 'Application submitted successfully (demo mode)'
  };
}

/**
 * Mock: Get available car brands
 */
export async function getBrands() {
  await new Promise(resolve => setTimeout(resolve, 200));
  return ['Perodua', 'Proton', 'Toyota', 'Honda', 'Nissan', 'Mazda', 'Hyundai', 'Kia'];
}

/**
 * Mock: Get models for a specific brand
 */
export async function getModels(brand) {
  await new Promise(resolve => setTimeout(resolve, 200));
  
  const modelMap = {
    'Perodua': ['Myvi', 'Axia', 'Bezza', 'Alza', 'Ativa'],
    'Proton': ['Saga', 'Persona', 'Iriz', 'X50', 'X70'],
    'Toyota': ['Vios', 'Camry', 'Corolla', 'Hilux', 'Fortuner'],
    'Honda': ['City', 'Civic', 'Accord', 'CR-V', 'HR-V'],
    'Nissan': ['Almera', 'Sentra', 'Teana', 'X-Trail', 'Navara'],
    'Mazda': ['Mazda2', 'Mazda3', 'Mazda6', 'CX-3', 'CX-5'],
    'Hyundai': ['i10', 'i20', 'Elantra', 'Sonata', 'Tucson'],
    'Kia': ['Picanto', 'Rio', 'Cerato', 'Optima', 'Sportage']
  };
  
  return modelMap[brand] || [];
}

/**
 * Mock: Health check
 */
export async function healthCheck() {
  return { status: 'healthy', mode: 'mock' };
=======
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

// Mock: confirm ownership by last 4 digits (used by PlateSection)
export async function confirmOwnership(plateRaw, last4){
  await new Promise(r => setTimeout(r, 300));
  const plate = String(plateRaw || '').toUpperCase().replace(/\s+/g, '');
  const hit = VEHICLES.find(v => v.plate === plate);
  if (!hit) return { ok:false, message: 'Record not found.' };
  if (String(last4) === hit.ownerLast4) {
    return { ok:true, personal: hit.personal, car: hit.car };
  }
  return { ok:false, message: 'Last 4 digits do not match.' };
>>>>>>> Stashed changes
}

