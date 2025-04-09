from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Max, Min, Q, F, Sum, Case, When
from django.db.models.signals import pre_save, post_save, post_delete
from django.utils import timezone
import datetime
from django.utils.text import slugify
# Create your models here.
from movie_recommendation_engine.common.models import PublishStateOptions
from movie_recommendation_engine.common.receivers import unique_slugify_pre_save, publish_state_pre_save
from movie_recommendation_engine.categories.models import Category
from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.tags.models import TaggedItem
from movie_recommendation_engine.videos.models import Video

RATING_CALC_TIME_IN_DAYS = 3

class PlaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte= now 
        )
    def search(self, query=None):
        if query is None:
            return self.none()
        return self.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query) | 
            Q(category__title__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(tags__tag__icontains=query)
        ).distinct()

    def movie_or_show(self):
        return self.filter(
            Q(type=Playlist.PlaylistTypeChoices.MOVIE) |
            Q(type=Playlist.PlaylistTypeChoices.SHOW)
        )
        
    def movies_shows_and_playlists(self):
        return self.filter(
            Q(type=Playlist.PlaylistTypeChoices.MOVIE) |
            Q(type=Playlist.PlaylistTypeChoices.SHOW) |
            Q(type=Playlist.PlaylistTypeChoices.PLAYLIST)
        )
        
        
    def popular(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.order_by(ordering)
    
    def popular_calc(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.annotate(score=Sum(
                F('rating_avg') * F('rating_count'),
                output_field=models.FloatField()
            )
        ).order_by(ordering)

    def needs_updating(self):
        now = timezone.now()
        days_ago = now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS)
        return self.filter(
            Q(rating_last_updated__isnull=True)|
            Q(rating_last_updated__lte=days_ago)
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured_playlists(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.PLAYLIST)
    
    def by_id_order(self, movie_pks=[]):
        qs = self.get_queryset().filter(pk__in=movie_pks)
        maintain_order = Case(*[When(pk=pki, then=idx) for idx, pki in enumerate(movie_pks)])
        return qs.order_by(maintain_order)
    
    def needs_updating(self):
        return self.get_queryset().needs_updating()



class Playlist(models.Model):
    '''
    MOVIE =>parent = null (does not have a parent)
            related = blank (does not have a list of other movies or tvshows)
            video = one video (movie)
            videos = blank
    
    TVSHOW =>parent = null (does not have a parent becouse it is the parent)
            related = blank (does not have a list of other movies or tvshows)
            video = one video (TVSHOW trailer)
            videos = List of Seasons(episodes)
            
    SEASON => parent = True (The TVSHOW)
            related = blank (does not have a list of other movies or tvshows)
            video = one video (SEASON trailer)
            videos = List of videos(episodes)
    
    PLAYLIST => parent = null (does not have a parent)
                related = List of other movies or tvshows
                video = Blank
                videos = List of videos
    
    '''
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = "MOV", "Movie"
        SHOW = 'TVS', "TV Show"
        SEASON = 'SEA', "Season"
        PLAYLIST = 'PLY', "Playlist"
    
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL) # For Seasons => The parent is the TvShow Name
    related = models.ManyToManyField("self", blank=True, through='PlaylistRelated') # For Playlists (List of Movies and TvShows) 
    video = models.ForeignKey(Video, related_name='playlist_featured', blank=True, null=True, on_delete=models.SET_NULL) # ONE VIDEO => For  Movie(Movie) | TVshow(Trailer) | Season(Trailer)
    videos = models.ManyToManyField(Video, related_name='playlist_item', blank=True, through='PlaylistItem') # LIST OF VIDEO => for Season(episodes) | Playlist(videos)
    
    category = models.ManyToManyField(Category, related_name='playlists', blank=True)
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    order = models.IntegerField(default=1)
    title = models.CharField(max_length=220)
    type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices, default=PlaylistTypeChoices.PLAYLIST)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True, auto_now=False, auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    poster_path = models.CharField(max_length=220, blank=True, null=True)
    # Rating
    ratings = GenericRelation(Rating, related_query_name='playlist')
    rating_last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True) # 5.00, 0.00
    score = models.FloatField(blank=True, null=True)
    idx = models.IntegerField(help_text='Position IDs for ML', blank=True, null=True)
    
    objects = PlaylistManager()
    
    def __str__(self):
        if not self.release_date:
            return f"{self.title}"
        return f"{self.title} ({self.release_date.year})"

    def get_related_items(self):
        return self.playlistrelated_set.all()

    def get_absolute_url(self):
        if self.is_movie:
            return f"/movies/{self.slug}/"
        if self.is_show:
            return f"/shows/{self.slug}/"
        if self.is_season and self.parent is not None:
            return f"/shows/{self.parent.slug}/seasons/{self.slug}/"
        return f"/playlists/{self.slug}/"

    @property
    def is_season(self):
        return self.type == self.PlaylistTypeChoices.SEASON

    @property
    def is_movie(self):
        return self.type == self.PlaylistTypeChoices.MOVIE

    @property
    def is_show(self):
        return self.type == self.PlaylistTypeChoices.SHOW

    # def get_rating_avg(self):
    #     return Playlist.objects.filter(id=self.id).aggregate(Avg("ratings__value"))

    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(max=Max("ratings__value"), min=Min("ratings__value"))

    # def get_short_display(self):
    #     return ""

    def get_video_id(self):
        """
        get main video id to render video for users
        """
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        """
        get clips to render clips for users
        """
        return self.playlistitem_set.all().published()

    @property
    def is_published(self):
        return self.active
    
    
    # def rating_avg_display(self):
    #     now = timezone.now()
    #     if not self.rating_last_updated:
    #         return self.calculate_rating()
    #     if self.rating_last_updated > now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS):
    #         return self.rating_avg
    #     return self.calculate_rating()

    # def calculate_ratings_count(self):
    #     return self.ratings.all().count()
    
    # def calculate_ratings_avg(self):
    #     return self.ratings.all().avg()

    # def calculate_rating(self, save=True):
    #     rating_avg = self.calculate_ratings_avg()
    #     rating_count = self.calculate_ratings_count()
    #     self.rating_count= rating_count
    #     self.rating_avg = rating_avg
    #     self.rating_last_updated = timezone.now()
    #     if save:
    #         self.save()
    #     return self.rating_avg
    





class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)


class MovieProxy(Playlist):

    objects = MovieProxyManager()

    def get_movie_id(self):
        """
        get movie id to render movie for users
        """
        return self.get_video_id()
    
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args, **kwargs)



class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW)

class TVShowProxy(Playlist):

    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args, **kwargs)

    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

    



class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON)

class TVShowSeasonProxy(Playlist):

    objects = TVShowSeasonProxyManager()

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self, *args, **kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args, **kwargs)

    def get_season_trailer(self):
        """
        get trailer to render for users
        """
        return self.get_video_id()

    def get_episodes(self):
        """
        get episodes to render for users
        """
        qs = self.playlistitem_set.all().published()
        #print(qs)
        return qs
    



class PlaylistItemQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            playlist__state=PublishStateOptions.PUBLISH,
            playlist__publish_timestamp__lte= now,
            video__state=PublishStateOptions.PUBLISH,
            video__publish_timestamp__lte= now 
        )

class PlaylistItemManager(models.Manager):
    def get_queryset(self):
        return PlaylistItemQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


# List of video for Season(episodes) and Playlist(videos)
class PlaylistItem(models.Model): 
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PlaylistItemManager()

    class Meta:
        ordering = ['order', '-timestamp']



def pr_limit_choices_to():
    return Q(type=Playlist.PlaylistTypeChoices.MOVIE) |  Q(type=Playlist.PlaylistTypeChoices.SHOW)

class PlaylistRelated(models.Model):
    '''
    A Playlist can have a list of TVShow and Movie (related Playlists) 
    '''
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlists_related')
    related = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='related_item', limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)





pre_save.connect(publish_state_pre_save, sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowProxy)

pre_save.connect(publish_state_pre_save, sender=TVShowSeasonProxy)
pre_save.connect(unique_slugify_pre_save, sender=TVShowSeasonProxy)

pre_save.connect(publish_state_pre_save, sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save, sender=MovieProxy)

pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(unique_slugify_pre_save, sender=Playlist)