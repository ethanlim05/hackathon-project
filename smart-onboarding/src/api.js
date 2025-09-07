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
 * Returns:
 *  - { ok: true, message }
 *  - { ok: false, message, corrected?, errors? }
 */
export async function validateCar(car) {
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
 * Returns:
 *  - { ok: true, applicationId, message }
 *  - { ok: false, message }
 */
export async function submitOnboarding(payload) {
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
}

