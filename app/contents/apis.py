import random

from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from contents.models import Contents
from contents.serializers import ContentsDetailSerializer, ContentsSerializer, WatchingSerializer
from members.models import Profile, Watching


def get_ad_contents():
    max_id = Contents.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        contents = Contents.objects.filter(pk=pk).first()
        if contents:
            return contents


def get_top_contents():
    max_id = Contents.objects.filter(contents_pub_year='2020').aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        contents = Contents.objects.filter(pk=pk).first()
        if contents:
            return contents


class ContentsRetrieveListView(APIView):
    def get(self, request, profile_pk, contents_pk):
        contents = Contents.objects.get(pk=contents_pk)
        serializer = ContentsDetailSerializer(contents)
        profile = Profile.objects.get(pk=profile_pk)
        is_selected = True if profile in contents.select_profiles.all() else False
        is_like = True if profile in contents.like_profiles.all() else False
        data = {
            'contents': serializer.data,
            'is_selected': is_selected,
            'is_like': is_like,
        }
        return Response(data)


class ContentsLikeAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.like_profiles.all():
            contents.like_profiles.remove(profile)
        else:
            contents.like_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsSelectAPIView(APIView):
    def get(self, request, profile_pk, contents_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        contents = get_object_or_404(Contents, pk=contents_pk)

        if profile in contents.select_profiles.all():
            contents.select_profiles.remove(profile)
        else:
            contents.select_profiles.add(profile)

        return Response(status=status.HTTP_200_OK)


class ContentsListView(APIView):

    def get(self, request, profile_pk):
        profile = get_object_or_404(Profile, pk=profile_pk)
        all_contents = Contents.objects.all()
        recommand_contents = all_contents.filter(contents_pub_year='2020')[:10]
        top_contents = get_top_contents()
        ad_contents = get_ad_contents()
        preview_contents = Contents.objects.all()[:10]
        watching_video = Watching.objects.filter(profile=profile)

        serializer_all = ContentsSerializer(all_contents, many=True)
        serializer_recommand = ContentsSerializer(recommand_contents, many=True)
        serializer_preview = ContentsSerializer(preview_contents, many=True)
        serializer_top = ContentsDetailSerializer(top_contents)
        serializer_ad = ContentsDetailSerializer(ad_contents)
        serializer_watching_video = WatchingSerializer(watching_video, many=True)

        data = {
            "top_contents": serializer_top.data,
            "ad_contents": serializer_ad.data,
            "recommand_contents": serializer_recommand.data,
            "preview_contents": serializer_preview.data,
            "all_contents": serializer_all.data,
            "watcing_video": serializer_watching_video.data
        }
        return Response(data)
