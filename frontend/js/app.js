
async function fetchData(endpoint) {
    const response = await fetch(`${API_BASE_URL}/${endpoint}/`);

    if (!response.ok) {
        throw new Error(`Could not load ${endpoint}`);
    }

    return await response.json();
}

async function loadDashboard() {
    const errorMessage = document.getElementById("errorMessage");
    errorMessage.hidden = true;

    try {
        const [owners, properties, tenants, leases] =
            await Promise.all([
                fetchData("owners"),
                fetchData("properties"),
                fetchData("tenants"),
                fetchData("leases")
            ]);

        document.getElementById("ownerCount").textContent = owners.length;
        document.getElementById("propertyCount").textContent = properties.length;
        document.getElementById("tenantCount").textContent = tenants.length;
        document.getElementById("leaseCount").textContent = leases.length;

        displayProperties(properties);

    } catch (error) {
        errorMessage.textContent =
            error.message + ". Check whether your FastAPI server is running.";

        errorMessage.hidden = false;

        document.getElementById("propertyTable").innerHTML =
            `<tr><td colspan="5">Unable to load properties.</td></tr>`;
    }
}

function displayProperties(properties) {
    const table = document.getElementById("propertyTable");

    if (properties.length === 0) {
        table.innerHTML =
            `<tr><td colspan="5">No properties found.</td></tr>`;
        return;
    }

    table.innerHTML = "";

    properties.slice(0, 5).forEach(property => {
        const row = document.createElement("tr");

        const values = [
            property.id,
            property.title,
            property.property_type,
            `₹${property.monthly_rent}`,
            property.status
        ];

        values.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value ?? "-";
            row.appendChild(cell);
        });

        table.appendChild(row);
    });
}

document.addEventListener("DOMContentLoaded", loadDashboard);
