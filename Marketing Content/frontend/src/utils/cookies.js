export const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        const cookieValue = parts.pop().split(';').shift();
        // console.log(`Cookie [${name}]: ${cookieValue}`);
        return cookieValue;
    }
    console.log(`Cookie [${name}] not found`);
    return null;
};