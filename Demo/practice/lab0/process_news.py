import os
import csv
from collections import Counter
import nltk
from nltk.corpus import stopwords

def extract_keywords(text, num_keywords=3):
    # Tokenize and convert to lowercase
    words = text.lower().split()
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Count word frequencies
    word_freq = Counter(words)
    
    # Get the top keywords
    keywords = [word for word, _ in word_freq.most_common(num_keywords)]
    return keywords

def process_articles():
    articles_dir = "../sample_news_articles"
    output_file = "news_data.csv"
    
    # Download required NLTK data
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    
    # Store processed data
    processed_data = []
    
    # Process each article
    for filename in os.listdir(articles_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(articles_dir, filename), 'r', encoding='utf-8') as file:
                content = file.read().strip().split('\n')
                
                # Extract title and date from first lines
                title = content[0].strip()
                date = content[1].strip()
                
                # Join remaining content
                article_text = ' '.join(content[2:])
                
                # Extract keywords
                keywords = extract_keywords(article_text)
                
                # Add to processed data
                processed_data.append({
                    'Title': title,
                    'Date': date,
                    'Keywords': ', '.join(keywords)
                })
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Date', 'Keywords'])
        writer.writeheader()
        writer.writerows(processed_data)
        
    print(f"Processing complete. Results saved to {output_file}")

if __name__ == "__main__":
    process_articles()