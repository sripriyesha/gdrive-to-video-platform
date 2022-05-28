const fs = require('fs');

const addExitCallback = require('catch-exit').addExitCallback;
const puppeteer = require('puppeteer');

const userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36";

const { Command } = require('commander');
const { exit } = require('process');
const program = new Command();
program.version('0.0.1');

program
    .option('--cookies-file <path>', 'path to the browser cookies file to be logged in in JSON format')
    .option('--video-file <path>', 'local path to the video file to be uploaded');

addExitCallback((exitCode) => {
    if (exitCode !== 1) {
        return;
    }

    console.log();
    program.outputHelp();
});


try {
    program.parse(process.argv);
} catch (err) {
    exit(1);
}
shouldExit = false;

if (!program.cookiesFile) {
    console.warn('Cookies JSON file needs to be provided');
    shouldExit = true;
}

if (!program.videoFile) {
    console.warn('Video file path needs to be provided');
    shouldExit = true;
}

if (shouldExit) {
    exit(1);
}

function pathExistsOrWarn(path) {
    if (fs.existsSync(path)) {
        return true;
    }

    console.warn(path + ' does not exist.');
    console.warn('Please provide a correct path.');
    return false;
}

if (!pathExistsOrWarn(program.cookiesFile)) {
    shouldExit = true;
}
if (!pathExistsOrWarn(program.videoFile)) {
    shouldExit = true;
}
if (shouldExit) {
    exit(1);
}

// exit();

function isInt(value) {
    var x;
    if (isNaN(value)) {
        return false;
    }
    x = parseFloat(value);
    return (x | 0) === x;
}

(async () => {
    let browser;
    try {
        console.log("Opening the browser...");
        browser = await puppeteer.launch({
            headless: false,
            args: [
                "--disable-setuid-sandbox",
                '--start-maximized'
            ],
            'ignoreHTTPSErrors': true,
            executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        });
    } catch (err) {
        console.log("Could not create a browser instance => : ", err);
    }

    const page = await browser.newPage();
    await page.setViewport({ width: 1724, height: 768 });
    await page.setUserAgent(userAgent);

    console.log("Setting cookies...");
    const cookiesString = fs.readFileSync(program.cookiesFile);
    const cookies = JSON.parse(cookiesString);
    await page.setCookie(...cookies);


    try {
        process.stdout.write("Loading Bitchute upload page...");
        url = 'https://www.bitchute.com/myupload/';
        await page.goto(url, {
            waitUntil: 'networkidle0'
        });
        console.log('[DONE]');
    } catch (e) {
        console.log('[KO]');
        console.log(e);
        await browser.close();
        return;
    }

    await page.waitForTimeout(1000);

    const videoFilename = program.videoFile.replace('videos/', '');
    await page.$eval('#title', (el, value) => el.value = value, videoFilename);

    const inputUploadHandle = await page.$('input[type=file]');
    inputUploadHandle.uploadFile(program.videoFile);

    let isUploadComplete = false;

    await page.waitForSelector('span.filepond--file-status-main');

    while (!isUploadComplete) {
        uploadProgressMessage = await page.evaluate(
            element => element.textContent,
            await page.$('span.filepond--file-status-main')
        );

        isUploadComplete = uploadProgressMessage === 'Upload complete';

        await page.waitForTimeout(2000);
    }

    await page.evaluate(() => document.getElementById('thumbnailButton').click());

    let videoIsSubmitted = false;

    while (!videoIsSubmitted) {
        await page.$eval('button[type=submit]', el => el.click());

        try {
            await page.waitForSelector('#channel-title', {timeout: 5000});
            videoIsSubmitted = true
        } catch (e) {
        }
    }

    console.log("Video submitted successfully")

    try {
        process.stdout.write("Loading Bitchute channel page...");
        url = 'https://www.bitchute.com/channel/xv7nipogCLt1/';
        await page.goto(url, {
            waitUntil: 'networkidle0'
        });
        console.log('[DONE]');
    } catch (e) {
        console.log('[KO]');
        console.log(e);
        await browser.close();
        return;
    }

    await page.waitForTimeout(1000);

    //Get video link
    const hrefs = await Promise.all((
        await page.$x('//a[contains(@class, "spa") and contains(text(), "'+videoFilename+'")]')
    ).map(
        async item => await (
            await item.getProperty('href')
        ).jsonValue())
    );

    console.log(hrefs[0]);

    await browser.close();
})();
