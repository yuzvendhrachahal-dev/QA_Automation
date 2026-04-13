var latestTestResult = null;

function executeTest() {
  var url = document.getElementById("url").value;
  var stepsText = document.getElementById("steps").value;
  var testName = document.getElementById("testName").value;

  if (!url || !stepsText || !testName) {
    alert("Please fill all fields");
    return;
  }

  var steps = stepsText.split("\n").filter(function(s) { return s.trim() !== ""; });

  document.getElementById("loader").style.display = "block";
  document.getElementById("results").innerHTML = "";
  document.getElementById("downloadBtn").style.display = "none";

  fetch("http://127.0.0.1:5000/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url, steps: steps, testName: testName })
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    latestTestResult = data;
    console.log("RESPONSE:", JSON.stringify(data, null, 2));
    renderResults(data);
  })
  .catch(function(err) {
    document.getElementById("results").innerHTML = "<span style='color:red'>Error: " + err.message + "</span>";
    console.error(err);
  })
  .finally(function() {
    document.getElementById("loader").style.display = "none";
  });
}

function renderResults(data) {
  var container = document.getElementById("results");
  var html = "";

  html += "<h3>" + data.testName + "</h3>";
  html += "<p><b>Run ID:</b> " + data.runId + "</p>";

  var overallClass = data.status === "PASSED" ? "status-passed" : "status-failed";
  html += "<h4 class='" + overallClass + "'>Status: " + data.status + "</h4>";

  for (var s = 0; s < data.steps.length; s++) {
    var step = data.steps[s];
    var stepClass = step.status === "PASSED" ? "status-passed" : "status-failed";

    html += "<div class='step'>";
    html += "<b>Step " + step.stepNumber + "</b><br/>";
    html += step.description + "<br/>";
    html += "<span class='" + stepClass + "'>Status: " + step.status + "</span><br/>";

    if (step.error) {
      html += "<span style='color:red'>Error: " + step.error + "</span><br/>";
    }

    if (step.screenshot) {
      var sUrl = "http://127.0.0.1:5000/" + step.screenshot + "?t=" + Date.now();
      html += "<br/><img src='" + sUrl + "' width='500' style='margin-top:10px;border-radius:6px;'/><br/>";
    }

    if (step.events && step.events.length > 0) {
      html += "<div style='margin-top:16px;'>";
      html += "<h4 style='margin:0 0 10px;color:#1f2937;'>Event Validation Results (" + step.events.length + " events)</h4>";

      for (var e = 0; e < step.events.length; e++) {
        var ev = step.events[e];
        var expired = ev.status === "EXPIRED";
        var color = expired ? "#ef4444" : "#22c55e";
        var eUrl = "http://127.0.0.1:5000/" + ev.screenshot + "?t=" + Date.now();

        html += "<div style='border:2px solid " + color + ";border-radius:8px;padding:12px;margin:8px 0;background:#fff;'>";
        html += "<div style='display:flex;justify-content:space-between;margin-bottom:6px;'>";
        html += "<b>Event " + ev.event + ": " + ev.title + "</b>";
        html += "<span style='color:" + color + ";font-weight:700;border:1.5px solid " + color + ";padding:2px 10px;border-radius:20px;'>" + ev.status + "</span>";
        html += "</div>";
        html += "<div style='color:#6b7280;font-size:13px;margin-bottom:10px;'>Date: " + ev.date + "</div>";
        html += "<img src='" + eUrl + "' style='max-width:100%;border-radius:6px;border:1px solid #e5e7eb;'/>";
        html += "</div>";
      }

      html += "</div>";
    }

    html += "</div>";
  }

  container.innerHTML = html;
  document.getElementById("downloadBtn").style.display = "block";
}

function downloadReport() {
  if (!latestTestResult) {
    alert("No test result to download.");
    return;
  }

  var data = latestTestResult;
  var html = "";

  html += "<!DOCTYPE html><html><head><meta charset='UTF-8'/>";
  html += "<title>QA Report - " + data.testName + "</title>";
  html += "<style>";
  html += "body{font-family:Arial,sans-serif;margin:30px;color:#1f2937;background:#f5f7fb;}";
  html += "h1{color:#2563eb;}";
  html += ".step{background:#fff;margin:16px 0;padding:16px;border-left:5px solid #22c55e;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.06);}";
  html += ".step.failed{border-left-color:#ef4444;}";
  html += ".passed{color:#22c55e;font-weight:700;}";
  html += ".failed{color:#ef4444;font-weight:700;}";
  html += ".event-card{border:2px solid #22c55e;border-radius:8px;padding:12px;margin:8px 0;background:#fff;}";
  html += ".event-card.expired{border-color:#ef4444;}";
  html += "img{max-width:100%;border-radius:6px;margin-top:8px;}";
  html += "@media print{body{margin:10px;}button{display:none;}}";
  html += "</style></head><body>";

  html += "<h1>QA Test Report</h1>";
  html += "<p><b>Test Name:</b> " + data.testName + "</p>";
  html += "<p><b>Run ID:</b> " + data.runId + "</p>";
  html += "<p><b>Overall Status:</b> <span class='" + (data.status === "PASSED" ? "passed" : "failed") + "'>" + data.status + "</span></p>";
  html += "<hr/>";

  for (var s = 0; s < data.steps.length; s++) {
    var step = data.steps[s];
    var isStepFailed = step.status !== "PASSED";

    html += "<div class='step" + (isStepFailed ? " failed" : "") + "'>";
    html += "<b>Step " + step.stepNumber + ":</b> " + step.description + "<br/>";
    html += "<span class='" + (isStepFailed ? "failed" : "passed") + "'>Status: " + step.status + "</span>";

    if (step.error) {
      html += "<br/><span style='color:red'>Error: " + step.error + "</span>";
    }

    if (step.screenshot) {
      var sUrl = "http://127.0.0.1:5000/" + step.screenshot;
      html += "<br/><img src='" + sUrl + "' width='600'/>";
    }

    if (step.events && step.events.length > 0) {
      html += "<h4 style='margin:16px 0 8px;'>Event Validation Results (" + step.events.length + " events)</h4>";

      for (var e = 0; e < step.events.length; e++) {
        var ev = step.events[e];
        var expired = ev.status === "EXPIRED";
        var color = expired ? "#ef4444" : "#22c55e";
        var eUrl = "http://127.0.0.1:5000/" + ev.screenshot;

        html += "<div class='event-card" + (expired ? " expired" : "") + "' style='border-color:" + color + ";'>";
        html += "<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>";
        html += "<b>Event " + ev.event + ": " + ev.title + "</b>";
        html += "<span style='color:" + color + ";font-weight:700;border:1.5px solid " + color + ";padding:2px 10px;border-radius:20px;'>" + ev.status + "</span>";
        html += "</div>";
        html += "<div style='color:#6b7280;font-size:13px;margin-bottom:8px;'>Date: " + ev.date + "</div>";
        html += "<img src='" + eUrl + "' style='max-width:100%;border-radius:6px;'/>";
        html += "</div>";
      }
    }

    html += "</div>";
  }

  html += "<p style='color:#9ca3af;font-size:12px;margin-top:30px;'>Generated by QA Automation AI</p>";
  html += "</body></html>";

  // Open in new window and trigger print-to-PDF
  var win = window.open("", "_blank");
  win.document.write(html);
  win.document.close();

  // Wait for images to load then prompt print dialog (Save as PDF)
  win.onload = function() {
    setTimeout(function() {
      win.focus();
      win.print();
    }, 1500);
  };
}