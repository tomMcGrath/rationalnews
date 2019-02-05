echo "Loading Global Priorities"
python priorities.py > priorities.csv
echo "Accessing News Service"
python get_articles.py priorities.csv > articles_with_keywords.csv
echo "Computing QALY scores"
python score_articles.py priorities.csv articles_with_keywords.csv > ranked_articles.csv
