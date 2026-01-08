export interface Movie {
  movie_name: string;
  movie_link: string;
  fshare_link: string;
  original_title: string;
  genre: string;
  year: number | null;
  runtime: string | null;
  rating: number;
  overview: string;
  poster_url: string;
  backdrop_url: string;
  tmdb_id: string;
  category_id: number | null;
}

export interface Category {
  id: number;
  name: string;
  subcategories?: Category[];
}
