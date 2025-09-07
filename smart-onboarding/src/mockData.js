// Simple mock dataset so you can demo the UX without a real backend.
export const VEHICLES = [
    {
      plate: "JWD3000",
      ownerLast4: "4321",
      personal: {
        idType: "NRIC",
        idValue: "990101015555",
        fullName: "Aiman Hakim",
        email: "aiman@example.com",
        phone: "0123456789",
        addressLine1: "12, Jalan Teknologi",
        postcode: "47810",
        city: "Petaling Jaya",
        state: "Selangor",
        eHailing: false
      },
      car: { brand: "Perodua", model: "Myvi 1.5", year: "2020" }
    },
    {
      plate: "BJK1234",
      ownerLast4: "8877",
      personal: {
        idType: "NRIC",
        idValue: "010202088877",
        fullName: "Nurul Izzati",
        email: "nurul@example.com",
        phone: "0178887777",
        addressLine1: "33, Jalan Tun Razak",
        postcode: "50400",
        city: "Kuala Lumpur",
        state: "Wilayah Persekutuan",
        eHailing: true
      },
      car: { brand: "Honda", model: "City", year: "2019" }
    }
  ];
  