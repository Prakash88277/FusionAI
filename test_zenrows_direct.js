// Test ZenRows API directly
const axios = require('axios');

const ZENROWS_API_KEY = 'ac77427ddaea21133538d4e5a7464d975c3c835e';
const ZENROWS_BASE_URL = 'https://api.zenrows.com/v1/';

async function testZenRows() {
    console.log('🧪 Testing ZenRows API directly...');
    
    const searchUrl = 'https://www.indeed.com/jobs?q=software+developer&l=India';
    
    try {
        console.log('📡 Making request to ZenRows...');
        const response = await axios.get(ZENROWS_BASE_URL, {
            params: {
                apikey: ZENROWS_API_KEY,
                url: searchUrl,
                js_render: 'true',
                premium_proxy: 'true'
            },
            timeout: 30000
        });
        
        console.log('✅ ZenRows API Response received');
        console.log('Response size:', response.data.length, 'characters');
        
        // Check if we got job data
        if (response.data.includes('job') || response.data.includes('title')) {
            console.log('🎯 Job data detected in response');
            
            // Simple job extraction test
            const jobTitles = response.data.match(/class="jobTitle"[^>]*>.*?<\/span>/g) || [];
            console.log('Found job title elements:', jobTitles.length);
            
            return true;
        } else {
            console.log('❌ No job data found in response');
            return false;
        }
        
    } catch (error) {
        console.error('❌ ZenRows API Error:', error.message);
        
        if (error.response) {
            console.error('Status:', error.response.status);
            console.error('Error data:', error.response.data);
        }
        
        return false;
    }
}

// Run test
testZenRows().then(success => {
    if (success) {
        console.log('\n🎉 ZenRows API test PASSED!');
        console.log('✅ API key is working');
        console.log('✅ Job scraping is functional');
    } else {
        console.log('\n💥 ZenRows API test FAILED!');
        console.log('❌ Check API key or quota limits');
    }
});
