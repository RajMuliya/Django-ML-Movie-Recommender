from django.db import models 
# from django.contrib.auth.models import User

# Create your models here. 
class movie_list(models.Model): 
	movies = models.CharField(max_length=20) 
	

	def __str__(self): 
		return f"{self.movies}"
	

# class SearchHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
#     movie_name = models.CharField(max_length=255)  # Store the movie name
#     search_time = models.DateTimeField(auto_now_add=True)  # Store when the search was made

#     def __str__(self):
#         return f"{self.user.username} - {self.movie_name}"
