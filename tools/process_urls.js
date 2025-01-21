#!/usr/bin/env node

import { crawlWeChatArticle } from './crawler.js';
import fs from 'fs/promises';
import path from 'path';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function askQuestion(query) {
  return new Promise(resolve => {
    rl.question(query, resolve);
  });
}

async function processUrls() {
    try {
        const filePath = await askQuestion('Please enter the file path containing WeChat article URLs: ');
        if(!filePath){
          console.error('No path was provided.');
          process.exit(1);
         }
        const fileContent = await fs.readFile(filePath.trim(), 'utf-8');
        const urls = fileContent.split('\n').filter(Boolean).map(url => url.trim());

        if (urls.length === 0) {
             console.error('No URLs found in the file.');
             process.exit(1);
         }

        console.log(`Processing ${urls.length} URL(s) from file:`, filePath);

        for (const url of urls) {
            console.log('Processing URL:', url);
           try{
             const article = await crawlWeChatArticle(url);
            console.log('Article title:', article.title);

             // Generate filename from article title
           const filename = `${article.title.replace(/[<>:"/\\|?*]/g, '_')}.md`;
               const fullFilePath = path.join(path.dirname(filePath),filename)
            await fs.writeFile(fullFilePath, article.content);
            console.log('Content saved to:', fullFilePath);
          }catch(error){
            console.error('Failed to process article:', url, error);
         }
      }

    } catch (error) {
        console.error('Failed to read the file:', error);
    } finally{
       rl.close();
    }
}

processUrls();
