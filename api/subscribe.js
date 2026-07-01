export default async function handler(req, res) {
  // Enable CORS for Vercel
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  // Handle preflight request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { email } = req.body;
  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  const apiKey = process.env.SYSTEMEIO_API_KEY || '36ztyx4nsjj2nssdjqf1z2wn38r25u5go808nkcywujg3kv3ne9zl1303kelw0pp';
  const tagId = 2070083; // Tag for Brain Games Lead Magnet

  try {
    // 1. Create contact in Systeme.io
    const createRes = await fetch('https://api.systeme.io/api/contacts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-API-Key': apiKey
      },
      body: JSON.stringify({ email: email })
    });

    const contactData = await createRes.json();

    // 201: Created, 409: Conflict (already exists), 422: Unprocessable Entity (could exist)
    if (createRes.status === 201 || createRes.status === 409 || createRes.status === 422) {
      let contactId = contactData.id;

      // If contact already existed, try to fetch it to get the ID (since 409/422 might not return the full contact object)
      if (!contactId && email) {
        try {
          const searchRes = await fetch(`https://api.systeme.io/api/contacts?email=${encodeURIComponent(email)}`, {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'X-API-Key': apiKey
            }
          });
          const searchData = await searchRes.json();
          if (searchData.items && searchData.items.length > 0) {
            contactId = searchData.items[0].id;
          }
        } catch (searchErr) {
          console.error('Failed to search contact:', searchErr);
        }
      }

      // 2. Assign Tag to contact
      if (contactId) {
        try {
          await fetch(`https://api.systeme.io/api/contacts/${contactId}/tags`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'X-API-Key': apiKey
            },
            body: JSON.stringify({ tagId: tagId })
          });
        } catch (tagErr) {
          console.error('Failed to assign tag:', tagErr);
        }
      }

      return res.status(200).json({ success: true, contactId });
    }

    return res.status(createRes.status).json({ success: false, ...contactData });

  } catch (error) {
    console.error('Systeme.io subscription error:', error);
    return res.status(500).json({ error: 'Internal Server Error', details: error.message });
  }
}
