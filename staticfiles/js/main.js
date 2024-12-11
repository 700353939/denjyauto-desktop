document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('reprForClient');

    function createElement(tag, className = '', content = '') {
        const element = document.createElement(tag);
        if (className) {
            element.className = className;
        }
        if (content) {
            element.textContent = content;
        }
        return element;
    }

    function showLoading() {
        const loading = createElement('div', 'loading', 'Loading...');
        app.textContent = '';
        app.appendChild(loading);
    }

    function showLoginForm() {
        const loginForm = createElement('div', 'login-form');
        const usernameInput = createElement('input', 'username-input');
        usernameInput.placeholder = 'Username';
        const passwordInput = createElement('input', 'password-input');
        passwordInput.type = 'password';
        passwordInput.placeholder = 'Password';
        const loginButton = createElement('button', 'login-button', 'Login');

        loginButton.addEventListener('click', async () => {
            const username = usernameInput.value;
            const password = passwordInput.value;
            showLoading();
            const token = await login(username, password);
            if (token) {
                localStorage.setItem('authToken', token);
                showClientDashboard(token);
            } else {
                alert('Login failed');
                showLoginForm();
            }
        });

        loginForm.append(usernameInput, passwordInput, loginButton);
        app.textContent = '';
        app.appendChild(loginForm);
    }

    async function login(username, password) {
        try {
            const response = await fetch('https://denjyauto-e7a4hre3acf2dzfg.italynorth-01.azurewebsites.net/api/login/', { // HERE
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                return data.access;
            } else {
                console.error('Login failed:', data);
                return null;
            }
        } catch (error) {
            console.error('Error during login:', error);
            return null;
        }
    }

    async function showClientDashboard(token) {
        const dashboard = createElement('div', 'dashboard');
        const logoutButton = createElement('button', 'logout-button', 'Logout');
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('authToken');
            showLoginForm();
        });

        document.querySelectorAll('.logo, .main-button').forEach(el => el.remove());
        showLoading();
        const cars = await fetchData('/cars/', token);
        const carSection = createElement('div', 'car-section');

        for (const car of cars) {
            const carDiv = createElement('div', 'car');
            carDiv.textContent = `License Plate: ${car.license_plate}, Brand: ${car.brand}, Year: ${car.year}`;

            const repairs = await fetchData(`/repairs/?car_id=${car.id}`, token);
            if (repairs.length > 0) {
                const repairTable = createElement('table', 'repair-table');
                const tableHeader = createElement('thead');
                const headerRow = createElement('tr');
                ['Repair KM', 'Type', 'Price'].forEach(headerText => {
                    const th = createElement('th', '', headerText);
                    headerRow.appendChild(th);
                });
                tableHeader.appendChild(headerRow);

                const repairTbody = createElement('tbody');
                repairs.forEach(repair => {
                    const repairRow = createElement('tr');
                    ['repair_km', 'repairs_type_field', 'repair_price'].forEach(key => {
                        const td = createElement('td', '', repair[key]);
                        repairRow.appendChild(td);
                    });
                    repairTbody.appendChild(repairRow);
                });

                repairTable.append(tableHeader, repairTbody);
                carDiv.appendChild(repairTable);
            }

            carSection.appendChild(carDiv);
        }

        const changePasswordButton = createElement('button', 'change-password-button', 'Change Password');
        changePasswordButton.addEventListener('click', () => {
            showChangePasswordForm(token);
        });

        dashboard.append(logoutButton, changePasswordButton, carSection);
        app.textContent = '';
        app.appendChild(dashboard);
    }

    async function fetchData(endpoint, token) {
        try {
            const response = await fetch(`https://denjyauto-e7a4hre3acf2dzfg.italynorth-01.azurewebsites.net/api${endpoint}`, { // HERE
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }

    function showChangePasswordForm(token) {
        const form = createElement('div', 'change-password-form');
        const oldPasswordInput = createElement('input', 'old-password-input');
        oldPasswordInput.placeholder = 'Old Password';
        oldPasswordInput.type = 'password';
        const newPasswordInput = createElement('input', 'new-password-input');
        newPasswordInput.placeholder = 'New Password';
        newPasswordInput.type = 'password';
        const confirmNewPasswordInput = createElement('input', 'confirm-new-password-input');
        confirmNewPasswordInput.placeholder = 'Confirm New Password';
        confirmNewPasswordInput.type = 'password';
        const submitButton = createElement('button', 'submit-button', 'Change Password');

        submitButton.addEventListener('click', async () => {
            const oldPassword = oldPasswordInput.value;
            const newPassword = newPasswordInput.value;
            const confirmNewPassword = confirmNewPasswordInput.value;

            if (newPassword !== confirmNewPassword) {
                alert('Passwords do not match');
                return;
            }

            const success = await changePassword(token, oldPassword, newPassword);
            if (success) {
                alert('Password changed successfully');
                showClientDashboard(token);
            } else {
                alert('Failed to change password');
            }
        });

        form.append(oldPasswordInput, newPasswordInput, confirmNewPasswordInput, submitButton);
        app.textContent = '';
        app.appendChild(form);
    }

    async function changePassword(token, oldPassword, newPassword) {
        try {
            const response = await fetch('https://denjyauto-e7a4hre3acf2dzfg.italynorth-01.azurewebsites.net/api/change-password/', { // HERE
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({
                    old_password: oldPassword,
                    new_password: newPassword,
                    confirm_new_password: newPassword,
                }),
            });
            return response.ok;
        } catch (error) {
            console.error('Error changing password:', error);
            return false;
        }
    }

    const savedToken = localStorage.getItem('authToken');
    if (savedToken) {
        showClientDashboard(savedToken);
    } else {
        showLoginForm();
    }
});