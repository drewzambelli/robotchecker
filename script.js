async function checkRobots() {
    const urlInput = document.getElementById("urlInput").value.trim();
    
    if (!urlInput) {
        alert("Please enter a URL.");
        return;
    }

    let url = urlInput.startsWith("http://") || urlInput.startsWith("https://") ? urlInput : `http://${urlInput}`;
    
    try {
        const parsedUrl = new URL(url);
        const robotsUrl = `https://corsproxy.io/?${encodeURIComponent(parsedUrl.origin + "/robots.txt")}`;

        const response = await fetch(`https://corsproxy.io/?${encodeURIComponent(robotsUrl)}`);

        if (!response.ok) {
            document.getElementById("result").value = `No robots.txt found at ${robotsUrl}.`;
            return;
        }

        const robotsTxt = await response.text();
        const parsedData = parseRobotsTxt(robotsTxt);
        
        document.getElementById("result").value = formatParsedData(parsedData);
    } catch (error) {
        document.getElementById("result").value = `Error checking robots.txt: ${error.message}`;
    }
}

function parseRobotsTxt(robotsTxt) {
    const userAgents = {};
    let currentAgent = null;
    const lines = robotsTxt.split("\n");

    for (const line of lines) {
        const trimmedLine = line.trim();
        
        if (!trimmedLine || trimmedLine.startsWith("#")) continue;

        const [directive, value] = trimmedLine.split(":").map(item => item.trim());

        if (directive.toLowerCase() === "user-agent") {
            currentAgent = value;
            userAgents[currentAgent] = { Disallow: [], Allow: [] };
        } else if (directive.toLowerCase() === "disallow" && currentAgent) {
            userAgents[currentAgent].Disallow.push(value || "/");
        } else if (directive.toLowerCase() === "allow" && currentAgent) {
            userAgents[currentAgent].Allow.push(value || "/");
        }
    }

    return userAgents;
}

function formatParsedData(parsedData) {
    let formattedText = "";
    
    for (const [agent, rules] of Object.entries(parsedData)) {
        formattedText += `User-agent: ${agent}\n`;
        formattedText += `Disallowed paths: ${rules.Disallow.length ? rules.Disallow.join(", ") : "None"}\n`;
        formattedText += `Allowed paths: ${rules.Allow.length ? rules.Allow.join(", ") : "None"}\n\n`;
    }

    return formattedText || "No specific rules found.";
}

function exportCSV() {
    const urlInput = document.getElementById("urlInput").value.trim();
    const result = document.getElementById("result").value.trim();

    if (!urlInput || !result) {
        alert("Nothing to export. Please check a robots.txt file first.");
        return;
    }

    const csvContent = `Website URL,Robots.txt Content\n"${urlInput}","${result.replace(/\n/g, " ")}"`;
    
    const blob = new Blob([csvContent], { type: "text/csv" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "robots.txt_export.csv";
    a.click();
}
